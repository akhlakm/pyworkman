import os
import zmq
import signal
import random
import pylogg as log

from workman import conf
from workman import protocol as pr
from workman.service import Service

class ServiceManager(object):
    def __init__(self, bind_url, zmq_context = None) -> None:
        self._bind_url = bind_url
        self._context = zmq_context if zmq_context \
            else zmq.Context.instance()
        self._stop = False
        self._socket : zmq.Socket = None
        self._services  : dict[bytes, Service] = {}

    def start(self):
        if self._socket:
            raise RuntimeError("Socket already bound")
        
        self._init_encryption()
        self._socket = self._context.socket(zmq.ROUTER)
        self._socket.rcvtimeo = int(pr.HBEAT_INTERVAL * 1000)
        self._socket.bind(self._bind_url)
        log.info("ServiceManager listening on {}", self._bind_url)

        try:
            while not self._stop:
                try:
                    msg = self.receive()
                    if msg:
                        if msg.sender == pr.CLIENT:
                            self._handle_client_message(msg)
                        elif msg.sender == pr.WORKER:
                            self._handle_worker_message(msg)
                        else:
                            log.warn("Unknown sender: {}", msg.sender)
                except Exception as err:
                    log.error("Message handling failed: {}", err)

        finally:
            self.close()
    
    def shutdown(self):
        self._stop = True
        self.close()
        log.note("ServiceManager shutdown.")

    def close(self):
        if not self._socket:
            return
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.disconnect(self._bind_url)
        self._socket.close()
        self._socket = None

    def receive(self):
        while True:
            for name, svc in self._services.items():
                try:
                    svc.run()
                except Exception as err:
                    log.error("Service {} run failed: {}", name, err)

            try:
                frames = self._socket.recv_multipart()
                return pr.Message.parse(frames)
            except Exception as err:
                print(err)
                if self._socket is None or self._stop:
                    return

    def _init_encryption(self, key_file = "mgr.key"):
        if not conf.WorkMan.enable_encryption:
            log.warn("Encryption not enabled.")
            return
        try:
            keys = open(key_file).read().encode("utf-8").split(b"\n")
            random.shuffle(keys)
            log.note("Encryption keys loaded")
        except:
            keys = [pr.encryption_key() for i in range(10)]
            open(key_file, "w").write(b"\n".join(keys).decode("utf-8"))
            os.chmod(key_file, 0o600)
            log.note("New encryption keys saved")

        pr.Encryptor = pr.encryptor(*keys)

    def _handle_worker_message(self, msg : pr.Message):
        # log.trace("Received from worker: {}", msg.identity)
        # Get the associated service.
        if msg.service not in self._services:
            self._services[msg.service] = Service(msg.service, self._socket)
        svc = self._services[msg.service]

        if msg.action == pr.READY:
            svc.worker_ready(msg)

        elif msg.action == pr.HBEAT:
            svc.worker_beat(msg)

        elif msg.action == pr.UPDATE:
            svc.worker_update(msg)

        elif msg.action == pr.DONE:
            svc.worker_done(msg)

        elif msg.action == pr.GONE:
            svc.worker_gone(msg)

        elif msg.action == pr.REPLY:
            svc.worker_reply(msg)

    def _reply_client(self, msg, response : str):
        reply = pr.Message(pr.MANAGER, pr.REPLY, msg.service, msg.job, response)
        reply.set_identity(msg.identity)
        self._socket.send_multipart(reply.frames())

    def _handle_client_message(self, msg : pr.Message):
        # log.trace("Received from client: {}", msg.identity)
        if msg.action == pr.LIST:
            return self._handle_list_request(msg)
    
        # Get the associated service.
        if msg.service not in self._services:
            self._services[msg.service] = Service(msg.service, self._socket)
        svc = self._services[msg.service]

        # New job
        if msg.action == pr.REQUEST:
            reply = svc.client_new_job(msg)
            self._reply_client(msg, reply)

        # Job status
        elif msg.action == pr.STATUS:
            reply = svc.client_query_job(msg)
            self._reply_client(msg, reply)

        # Cancel job
        elif msg.action == pr.ABORT:
            svc.client_cancel_job(msg)

        # Service definition
        elif msg.action == pr.READY:
            reply = svc.job_definition()
            self._reply_client(msg, reply)


    def _handle_list_request(self, msg : pr.Message):
        if msg.service in [None, "None", ""]:
            # List all items
            svclist = {}
            for name, svc in self._services.items():
                svclist[name] = {
                    'jobs': svc.list_jobs(),
                    'workers': svc.list_workers(),
                    'definition': svc.job_definition(),
                }
        else:
            svclist = {
                'jobs': [],
                'workers': [],
                'definition': {},
            }
            if msg.service in self._services:
                svc = self._services[msg.service]
                svclist['jobs'] = svc.list_jobs()
                svclist['workers'] = svc.list_workers()
                svclist['definition'] = svc.job_definition()

        reply = pr.serialize(svclist)
        self._reply_client(msg, reply)


def start():
    log.init(conf.WorkMan.log_level, logfile_name="mgr.log", append_to_logfile=True)

    mgr = ServiceManager(bind_url=conf.WorkMan.mgr_url)
    def _sig_handler(sig, _):
        mgr.shutdown()

    signal.signal(signal.SIGINT, _sig_handler)
    signal.signal(signal.SIGTERM, _sig_handler)

    try:
        mgr.start()
    except Exception as err:
        print(err)

if __name__ == '__main__':
    start()
