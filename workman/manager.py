import zmq
import signal
from workman import protocol as pr
from workman.service import Service

class Manager(object):
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
        
        self._socket = self._context.socket(zmq.ROUTER)
        self._socket.rcvtimeo = int(pr.HBEAT_INTERVAL * 1000)
        self._socket.bind(self._bind_url)
        print("Manager listening on", self._bind_url)

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
                            print("Unknown sender")
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

    def receive(self):
        while True:
            try:
                frames = self._socket.recv_multipart()
                return pr.Message.parse(frames)
            except zmq.error.Again:
                print("Manager receive error.")
                if self._socket is None or self._stop:
                    return

    def _handle_worker_message(self, msg : pr.Message):
        # Get the associated service.
        if msg.service not in self._services:
            self._services[msg.service] = Service(self._socket)
        svc = self._services[msg.service]

        if msg.action == pr.READY:
            svc.worker_register(msg)

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

    def reply_client(self, msg, response):
        reply = pr.Message(pr.MANAGER, pr.REPLY, msg.service, msg.job, response)
        reply.set_identity(msg.identity)
        self._socket.send_multipart(msg.frames())

    def _handle_client_message(self, msg : pr.Message):
        # Get the associated service.
        if msg.service not in self._services:
            self._services[msg.service] = Service(self._socket)
        svc = self._services[msg.service]

        # New job
        if msg.action == pr.REQUEST:
            svc.client_new_job(msg)

        # Job status
        elif msg.action == pr.STATUS:
            reply = svc.client_query_job(msg)
            self.reply_client(msg, reply)

        # Cancel job
        elif msg.action == pr.ABORT:
            svc.client_cancel_job(msg)


def main():
    from util import conf
    mgr = Manager(bind_url=conf.WorkMan.mgr_url)

    def _sig_handler(sig, _):
        print("\nShutting down ...")
        mgr.shutdown()

    signal.signal(signal.SIGINT, _sig_handler)
    signal.signal(signal.SIGTERM, _sig_handler)

    mgr.start()

if __name__ == '__main__':
    main()
