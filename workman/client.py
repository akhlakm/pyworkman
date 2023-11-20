import zmq
from workman import protocol as pr

class Client(object):
    def __init__(self, manager_url, clientid = None, zmq_context=None):
        self.manager_url = manager_url
        self.identity = clientid
        self._socket : zmq.Socket = None
        self._zmq_context = zmq_context if zmq_context else zmq.Context.instance()
        self._expect_reply = False

    def _is_connected(self):
        return self._socket is not None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    def connect(self, reconnect=False):
        if reconnect:
            self.close()

        if self._is_connected():
            return

        self._socket = self._zmq_context.socket(zmq.DEALER)
        self._socket.setsockopt(zmq.LINGER, pr.ZMQ_LINGER)
        if self.identity:
            self._socket.setsockopt(zmq.IDENTITY, pr.encode(self.identity))
        self._socket.connect(self.manager_url)
        self._expect_reply = False

    def close(self):
        if not self._is_connected():
            return
        self._socket.setsockopt(zmq.LINGER, 0)
        self._socket.disconnect(self.manager_url)
        self._socket.close()
        self._socket = None
        self._expect_reply = False

    def request(self, service, job, message = None):
        msg = pr.Message(pr.CLIENT, pr.REQUEST, service, job, message)
        self._socket.send_multipart(msg.frames())
        self._expect_reply = True

    def status(self, service, job):
        msg = pr.Message(pr.CLIENT, pr.STATUS, service, job)
        self._socket.send_multipart(msg.frames())
        self._expect_reply = True

    def abort(self, service, job):
        msg = pr.Message(pr.CLIENT, pr.ABORT, service, job)
        self._socket.send_multipart(msg.frames())
        self._expect_reply = True

    def reply(self, timeout_sec : int = None) -> pr.Message:
        if not self._expect_reply:
            return None
        
        timeout = int(timeout_sec * 1000) if timeout_sec else None

        poller = zmq.Poller()
        poller.register(self._socket, zmq.POLLIN)

        try:
            socks = dict(poller.poll(timeout=timeout))

            if socks.get(self._socket) == zmq.POLLIN:
                self._expect_reply = False
                frames = self._socket.recv_multipart()
                return pr.Message.parse(frames)
            else:
                print("Error! Timed out waiting for reply from manager.")
        finally:
            poller.unregister(self._socket)


if __name__ == '__main__':
    with Client('tcp://127.0.0.1:5555', clientid='test-client') as client:
        client.request('test', '12', ['hello'])
        msg = client.reply(10)
        print(msg)
