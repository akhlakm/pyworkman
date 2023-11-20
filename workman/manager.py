import zmq
import time
import json
import signal
from workman import protocol as pr

class Worker:
    def __init__(self, service : bytes, workerid : bytes) -> None:
        self.id = workerid
        self.job = None
        self.service = service
        self._last_sent = 0.0
        self._last_update = 0.0
        self.gone = True
        self.ready = False
        self.busy = False

    def assign_job(self, jobid : bytes):
        self.job = jobid

class Job:
    def __init__(self, service : bytes, jobid : bytes, task : bytes) -> None:
        self.service = service
        self.id = jobid
        self.task = task
        self.result = None
        self.started = False
        self.cancelled = False
        self.done = False
        self.workerid : bytes = None
        self.updates : list[bytes] = []

    def __repr__(self) -> str:
        items = {
            k : v for k,v in self.__dict__.items()
            if not k.startswith("_")
        }
        return json.dumps(items)

    def assign_worker(self, workerid : bytes):
        self.workerid = workerid

class Service:
    def __init__(self, name : bytes) -> None:
        self.name = name
        self.job_queue : list[bytes] = []
        self.avail_workers : list[bytes] = []

    def add_job(self, jobid : bytes):
        self.job_queue.append(jobid)

    def add_worker(self, workerid : bytes):
        self.avail_workers.append(workerid)

    def remove_worker(self, workerid : bytes):
        try:
            self.avail_workers.remove(workerid)
        except ValueError:
            pass

    def process(self):
        if len(self.job_queue) and len(self.avail_workers):
            task = self.job_queue.pop(0)
            worker = self.avail_workers.pop(0)
            return task, worker
        return None


class Manager(object):
    def __init__(self, bind_url, zmq_context = None) -> None:
        self._bind_url = bind_url
        self._context = zmq_context if zmq_context else zmq.Context.instance()
        self._socket : zmq.Socket = None
        self._stop = False

        # works
        self._services  : dict[bytes, Service] = {}
        self._workers   : dict[bytes, Worker] = {}
        self._jobs      : dict[bytes, Job] = {}

    def start(self):
        if self._socket:
            raise RuntimeError("Socket already bound")
        
        self._socket = self._context.socket(zmq.ROUTER)
        self._socket.rcvtimeo = int(pr.HBEAT_INTERVAL * 1000)
        self._socket.bind(self._bind_url)
        print("Manager listening on", self._bind_url)

        try:
            while not self._stop:
                try:
                    message = self.receive()
                    if message:
                        self._handle(message)
                except Exception as err:
                    print("Message handling failed:", err)
                    raise

        finally:
            self.close()
    
    def shutdown(self):
        self._stop = True

    def close(self):
        if not self._socket:
            return
        self._socket.disconnect(self._bind_url)
        self._socket.close()
        self._socket = None

    def reply_client(self, outgoing : pr.Message, incoming : pr.Message = None):
        if incoming:
            outgoing.set_identity(incoming.identity)
        self._last_sent = time.time()
        self._socket.send_multipart(outgoing.frames())

    def hbeat_worker(self, worker : Worker):
        pass

    def request_worker(self, worker : Worker, task : bytes):
        pass

    def abort_worker(self, worker : Worker):
        pass

    def receive(self):
        while True:
            try:
                frames = self._socket.recv_multipart()
                return pr.Message.parse(frames)
            except zmq.error.Again:
                if self._socket is None or self._stop:
                    return
                
    def _key(self, service : bytes, obj : bytes) -> bytes:
        return service + b"::" + obj

    def _new_worker(self, workerid, service):
        if service not in self._services:
            self._services[service] = Service(service)
        svc = self._services[service]

        workerkey = self._key(service, workerid)
        if workerkey not in self._workers:
            self._workers[workerkey] = Worker(service, workerid)
        svc.add_worker(workerid)

    def _new_job(self, task, jobid, service):
        if service not in self._services:
            self._services[service] = Service(service)
        svc = self._services[service]

        jobkey = self._key(service, jobid)
        if jobkey not in self._jobs:
            self._jobs[jobkey] = Job(service, jobid, task)
        svc.add_job(jobid)


    def _handle(self, msg : pr.Message):
        if msg.sender == pr.CLIENT:
            self._handle_client_message(msg)
        elif msg.sender == pr.WORKER:
            self._handle_worker_message(msg)
        else:
            print("Unknown sender")


    def _handle_worker_message(self, msg : pr.Message):
        worker : Worker = self._workers.get(
            self._key(msg.service, msg.identity), None)
        
        job : Job = None
        if worker:
            worker._last_update = time.time()
            if worker.job:
                jobkey = self._key(msg.service, worker.job)
                job = self._jobs[jobkey]

        if msg.action == pr.READY:
            self._new_worker(msg.identity, msg.service)

        elif worker and msg.action == pr.HBEAT:
            pass

        elif worker and msg.action == pr.UPDATE:
            if job:
                job.updates.append(msg.message)

        elif worker and msg.action == pr.DONE:
            worker.job = None
            self._new_worker(worker.id, worker.service)
            if job:
                job.done = True

        elif worker and msg.action == pr.GONE:
            pass

        elif worker and msg.action == pr.REPLY:
            pass


    def _handle_client_message(self, msg : pr.Message):
        jobkey = self._key(msg.service, msg.jobid)
        job : Job = self._jobs.get(jobkey, None)

        # New job
        if msg.action == pr.REQUEST:
            task = b" ".join(msg.message)
            self._new_job(task, msg.job, msg.service)

        # Job status
        elif msg.action == pr.STATUS:
            if job:
                response = str(job)
            else:
                response = "Job not found"
            reply = pr.Message(
                pr.MANAGER, pr.REPLY, msg.service, msg.job, response)
            self._send(reply, msg)

        # Cancel job
        elif msg.action == pr.ABORT:
            job.cancelled = True
            if job and job.workerid:
                workerkey = self._key(msg.service, job.workerid)
                worker = self._workers[workerkey]
                self.abort_worker(worker)


def main():
    from util import conf
    mgr = Manager(bind_url=conf.WorkMan.mgr_url)

    def _sig_handler(sig, _):
        print("\nShutting down ...")
        mgr.shutdown()

    signal.signal(signal.SIGTERM, _sig_handler)
    signal.signal(signal.SIGINT, _sig_handler)

    mgr.start()

if __name__ == '__main__':
    main()