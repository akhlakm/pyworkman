import zmq
import time
import pylogg
from workman import protocol as pr

class ServiceJob(object):
    def __init__(self, jobid, service, task) -> None:
        self.id = jobid
        self.service = service
        self.task = task
        self.queued = True
        self.running = False
        self.complete = False
        self.cancelled = False
        self.abandoned = False
        self.workerid = None
        self.updates = []
        self.result = None

    def __repr__(self) -> str:
        return str(self.id)

    def status(self) -> dict:
        items = {
            k : v for k,v in self.__dict__.items()
            if not k.startswith("_")
        }
        return items

    def set_done(self):
        self.running = False
        self.abandoned = False
        self.complete = True

    def set_cancel(self):
        self.cancelled = True
        self.running = False
        self.queued = False

    def set_start(self, workerid):
        self.workerid = workerid
        self.queued = False
        self.running = True

    def requeue(self):
        self.queued = True
        self.abandoned = False

    def set_abandoned(self):
        # Do not requeue, as we are not sure if the job was complete.
        self.running = False
        self.abandoned = True

    def set_update(self, update):
        self.updates.append(update)

    def set_result(self, result):
        self.result = result


class ServiceWorker(object):
    def __init__(self, workerid, service, socket) -> None:
        self.idle = True
        self.service = service
        self.id : bytes = workerid
        self.jobid : bytes = None
        self.jobtask : bytes = None
        self.definition : str = None
        self._socket : zmq.Socket = socket
        self._hb_timeout = pr.HBEAT_TIMEOUT
        self._hb_interval = pr.HBEAT_INTERVAL
        self._last_sent = 0.0
        self._last_received = 0.0

    def __repr__(self) -> str:
        return str(self.id)

    def _send(self, action, jobid = None, message = None):
        msg = pr.Message(action, self.service, jobid, message)
        msg.set_identity(self.id)
        self._last_sent = time.time()
        self._socket.send_multipart(msg.frames())

    def execute(self, jobid, jobtask):
        self.idle = False
        self.jobid = jobid
        self.jobtask = jobtask
        self._send(pr.REQUEST, self.jobid, self.jobtask)

    def alive(self) -> bool:
        return (time.time() - self._last_received) < self._hb_timeout

    def send_hbeat(self):
        ds = time.time() - self._last_sent
        dr = time.time() - self._last_received
        if ds > self._hb_interval:
            self._send(pr.HBEAT)

    def send_abort(self, jobid : bytes):
        if self.jobid == jobid:
            self._send(pr.ABORT)
            self.jobtask = None
            self.jobid = None

    def new_hbeat(self):
        self._last_received = time.time()
        if self.definition is None:
            self._send(pr.READY)

    def set_ready(self, definition : str):
        self._last_received = time.time()
        self.idle = True
        self.definition = definition

    def set_gone(self):
        self._last_received = time.time()
        self.idle = False

    def set_done(self):
        self._last_received = time.time()
        self.jobtask = None
        self.jobid = None
        self.idle = True


class Service(object):
    def __init__(self, name, socket) -> None:
        self.name = name
        self._socket : zmq.Socket = socket
        self.jobs : dict[bytes, ServiceJob] = {}
        self.workers : dict[bytes, ServiceWorker] = {}
        self.log = pylogg.New(self.name)


    def list_jobs(self):
        items = {
            "queued": [k for k, job in self.jobs.items() if job.queued],
            "running": [k for k, job in self.jobs.items() if job.running],
            "done": [k for k, job in self.jobs.items() if job.complete],
            "cancelled": [k for k, job in self.jobs.items() if job.cancelled],
            "abandoned": [k for k, job in self.jobs.items() if job.abandoned],
        }
        return items
    

    def list_workers(self):
        items = {
            "ready": [
                k for k, worker in self.workers.items()
                if worker.idle and worker.alive()
            ],
            "busy": [
                k for k, worker in self.workers.items()
                if not worker.idle and worker.alive()
            ],
            "disconnected": [
                k for k, worker in self.workers.items() if not worker.alive()
            ],
        }
        return items
    

    def _execute(self):
        """ Execute a single job. """
        joblist = [j for j in self.jobs.values() if j.queued]
        workerlist = [
            w for w in self.workers.values() if w.idle and w.alive()
        ]

        # self.log.trace("Execute Joblist: {}", joblist)
        # self.log.trace("Execute Workers: {}", workerlist)

        job = None
        if joblist:
            job = joblist.pop(0)

        worker = None
        if workerlist:
            worker = workerlist.pop(0)

        if job and worker:
            self.log.info("Executing job {} on {}", job.id, worker.id)
            job.set_start(worker.id)
            worker.execute(job.id, job.task)


    def run(self):
        self._execute()
        for name, worker in self.workers.items():
            worker.send_hbeat()


    def client_new_job(self, msg : pr.Message) -> str:
        if msg.job not in self.jobs:
            job = ServiceJob(msg.job, msg.service, msg.message)
            self.jobs[job.id] = job
            self.log.info("{} submitted new job {}", msg.identity, job.id)
            r = job.status()
        else:
            job = self.jobs[msg.job]
            r = job.status()
            if job.abandoned:
                job.requeue()
                self.log.info("{} requeued job {}", msg.identity, job.id)
            else:
                r['error'] = 'Job exists'
                self.log.warn("{} requested duplicate job {}", msg.identity,
                              job.id)
    
        return pr.serialize(r)


    def client_query_job(self, msg : pr.Message) -> str:
        """ Return job status """
        if msg.job not in self.jobs:
            r = {'error': 'Job not found'}
            self.log.error("{} queried unknown job {}", msg.identity, msg.job)
            self.log.error("Currently listed jobs: {}",
                            ", ".join([s for s in self.jobs.keys()]))
        else:
            r = self.jobs[msg.job].status()
        return pr.serialize(r)


    def client_cancel_job(self, msg : pr.Message):
        self.log.warn("{} cancelled job {}", msg.identity, msg.job)
        job = self.jobs.get(msg.job)
        if job:
            if job.running:
                worker = self.workers[job.workerid]
                worker.send_abort(msg.job)
            job.set_cancel()


    def job_definition(self) -> str:
        defn = None
        keys = [k for k in self.workers.keys()]
        if keys:
            defn = self.workers[keys[-1]].definition
        return defn


    def _get_or_create_worker(self, msg : pr.Message) -> ServiceWorker:
        if msg.identity not in self.workers:
            worker = ServiceWorker(msg.identity, msg.service, self._socket)
            self.workers[worker.id] = worker
            self.log.info("{} registered for '{}' jobs", msg.identity,
                          msg.service)
        return self.workers[msg.identity]


    def worker_ready(self, msg : pr.Message):
        worker = self._get_or_create_worker(msg)
        if worker.jobid:
            # job done was not called.
            job = self.jobs[worker.jobid]
            job.set_abandoned()

        worker.set_ready(msg.message)


    def worker_beat(self, msg : pr.Message):
        worker = self._get_or_create_worker(msg)
        worker.new_hbeat()    


    def worker_update(self, msg : pr.Message):
        worker = self.workers.get(msg.identity)
        if not worker:
            self.log.error(
                "Update received from unknown worker: {}", msg.identity)
        else:
            job = self.jobs.get(msg.job)
            assert job, "Update received for unknown job"
            assert worker.jobid == job.id, \
                "Update received from unassigned worker"
            job.set_update(msg.message)
            worker.new_hbeat()


    def worker_done(self, msg : pr.Message):
        worker = self.workers.get(msg.identity)
        if not worker:
            self.log.error(
                "Done received from unknown worker: {}", msg.identity)
        else:
            self.log.note("Worker {} job done: {}", msg.identity, msg.job)
            job = self.jobs.get(msg.job)
            assert job, "Done received for unknown job"
            assert worker.jobid == job.id, "Done message from unassigned worker"
            worker.set_done()
            job.set_done()


    def worker_gone(self, msg : pr.Message):
        worker = self.workers.get(msg.identity)
        if not worker:
            self.log.error(
                "Gone received from unknown worker: {}", msg.identity)
        else:
            self.log.warn("Worker {} gone", msg.identity)
            if worker.jobid:
                job = self.jobs[worker.jobid]
                job.set_abandoned()
            worker.set_gone()
            del self.workers[msg.identity]
    

    def worker_reply(self, msg : pr.Message):
        worker = self.workers.get(msg.identity)
        if not worker:
            self.log.error(
                "Reply received from unknown worker: {}", msg.identity)
        else:
            self.log.trace("Worker {} job result: {}", msg.identity, msg.job)
            job = self.jobs.get(msg.job)
            assert job, "Reply received for unknown job"
            assert worker.jobid == job.id, \
                "Reply received from unassigned worker"
            job.set_result(msg.message)
            worker.new_hbeat()
