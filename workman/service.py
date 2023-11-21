import zmq
import time
import json
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
        self.abondoned = False
        self.workerid = None
        self.updates = []
        self.result = None

    def status(self) -> dict:
        items = {
            k : v for k,v in self.__dict__.items()
            if not k.startswith("_")
        }
        return items

    def set_start(self):
        self.queued = False
        self.running = True

    def set_done(self):
        self.queued = False
        self.running = False
        self.complete = True

    def set_cancel(self):
        self.cancelled = True
        self.queued = False
        self.running = False

    def set_worker(self, workerid):
        self.workerid = workerid

    def set_abondoned(self):
        self.abondoned = True
        self.queued = True

    def set_update(self, update):
        self.updates.append(update)

    def set_result(self, result):
        self.result = result


class ServiceWorker(object):
    def __init__(self, workerid, service, socket) -> None:
        self.idle = True
        self.id = workerid
        self.service = service
        self.jobid : bytes = None
        self.jobtask : bytes = None
        self._socket : zmq.Socket = socket
        self._hb_timeout = pr.HBEAT_TIMEOUT
        self._hb_interval = pr.HBEAT_INTERVAL
        self._last_sent = time.time()
        self._last_received = time.time()

    def _send(self, action, jobid = None, message = None):
        msg = pr.Message(pr.MANAGER, action, self.service, jobid, message)
        msg.set_identity(self.id)
        self._last_sent = time.time()
        self._socket.send_multipart(msg.frames())

    def execute(self, jobid, jobtask):
        self.jobid = jobid
        self.jobtask = jobtask
        self._send(pr.REQUEST, self.jobid, self.jobtask)

    def send_hbeat(self):
        if (time.time() - self._last_sent) > self._hb_interval:
            self._send(pr.HBEAT)

    def send_abort(self, jobid : bytes):
        if self.jobid == jobid:
            self._send(pr.ABORT)
            self.jobtask = None
            self.jobid = None

    def new_hbeat(self):
        self._last_received = time.time()

    def set_ready(self):
        self._last_received = time.time()
        self.idle = True

    def set_gone(self):
        self.idle = False

    def set_done(self):
        self._last_received = time.time()
        self.jobtask = None
        self.jobid = None
        self.idle = True


class Service(object):
    def __init__(self, socket) -> None:
        self._socket : zmq.Socket = socket
        self.jobs : dict[bytes, ServiceJob] = {}
        self.workers : dict[bytes, ServiceWorker] = {}

    def list_jobs(self):
        return self.jobs.keys()
    
    def list_workers(self):
        return self.workers.keys()
    
    def _execute(self):
        """ Execute a single job. """
        joblist = [j for j in self.jobs.values() if j.queued]
        workerlist = [w for w in self.workers.values() if w.idle]

        job = None
        if joblist:
            job = joblist.pop(0)

        worker = None
        if workerlist:
            worker = workerlist.pop(0)

        if job and worker:
            job.set_worker(worker.id)
            worker.execute(job.id, job.task)

    def client_new_job(self, msg : pr.Message):
        job = ServiceJob(msg.job, msg.service, msg.message)
        self.jobs[job.id] = job

    def client_query_job(self, msg : pr.Message) -> bytes:
        """ Return job status """
        if msg.job not in self.jobs:
            r = {'error': 'Job not found'}
        else:
            r = self.jobs[msg.job].status()
        return pr.encode(json.dumps(r))

    def client_cancel_job(self, msg : pr.Message):
        job = self.jobs.get(msg.job)
        if job:
            if job.running:
                worker = self.workers[job.workerid]
                worker.send_abort(msg.job)
            job.set_cancel()

    def worker_register(self, msg : pr.Message):
        worker = ServiceWorker(msg.identity, msg.service, self._socket)
        self.workers[worker.id] = worker

    def worker_beat(self, msg : pr.Message):
        worker = self.workers.get(msg.identity)
        if worker:
            worker.new_hbeat()
    
    def worker_update(self, msg : pr.Message):
        worker = self.workers.get(msg.identity)
        assert worker, "Update received from unknown worker"

        job = self.jobs.get(msg.job)
        assert job, "Update received for unknown job"
        assert worker.jobid == job.id, "Update received from unassigned worker"
        job.set_update(msg.message)

    def worker_done(self, msg : pr.Message):
        worker = self.workers.get(msg.identity)
        assert worker, "Done received from unknown worker"

        job = self.jobs.get(msg.job)
        assert job, "Done received for unknown job"
        assert worker.jobid == job.id, "Done message from unassigned worker"
        worker.set_done()
        job.set_done()

    def worker_gone(self, msg : pr.Message):
        worker = self.workers.get(msg.identity)
        if worker:
            if worker.jobid:
                job = self.jobs[worker.jobid]
                job.set_abondoned()
            worker.set_gone()
            del self.workers[msg.identity]
    
    def worker_reply(self, msg : pr.Message):
        worker = self.workers.get(msg.identity)
        assert worker, "Reply received from unknown worker"

        job = self.jobs.get(msg.job)
        assert job, "Reply received for unknown job"
        assert worker.jobid == job.id, "Reply received from unassigned worker"
        job.set_result(msg.message)
        worker.new_hbeat()
