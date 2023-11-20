import zmq
import signal
from workman import protocol as pr

class Manager(object):
    def __init__(self, bind_url = "tcp://127.0.0.1:5555", zmq_context = None) -> None:
        self._bind_url = bind_url
        self._context = zmq_context if zmq_context else zmq.Context.instance()
        self._socket : zmq.Socket = None
        self._stop = False

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
                        self.handle(message)
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
                return pr.parse(frames)
            except zmq.error.Again:
                if self._socket is None or self._stop:
                    return
                
    def handle(self, msg : pr.Message):
        # echo
        reply = pr.Message(
            pr.MANAGER, pr.REPLY, msg.service, msg.job, msg.message)
        reply.set_addr(msg.address)
        self._socket.send_multipart(reply.frames())
        print("Message handled.")


def main():
    mgr = Manager()

    def _sig_handler(sig, _):
        print("\nShutting down ...")
        mgr.shutdown()

    signal.signal(signal.SIGTERM, _sig_handler)
    signal.signal(signal.SIGINT, _sig_handler)

    mgr.start()

if __name__ == '__main__':
    main()