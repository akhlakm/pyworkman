import zmq
import signal
from util import conf
from workman import protocol as pr

class Worker(object):
    def __init__(self, manager_url, service, context=None):
        self.service : service
        self.manager_url = manager_url
        self._zmq_context = context if context else zmq.Context.instance()
        self._socket : zmq.Socket = None
        self._poller : zmq.Poller = None
        self._hb_interval = pr.HBEAT_INTERVAL
        self._hb_timeout = pr.HBEAT_TIMEOUT

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
        self._socket.connect(self.manager_url)

        self._poller = zmq.Poller()
        self._poller.register(self._socket, zmq.POLLIN)
        self._send_ready()

    def close(self):
        if not self._is_connected():
            return
        self._send_gone()
        self._socket.setsockopt(zmq.LINGER, 0)
        self._poller.unregister(self._socket)
        self._socket.disconnect(self.manager_url)
        self._socket.close()
        self._socket = None

    def _send_ready(self):
        msg = pr.Message(pr.WORKER, pr.READY, self.service)
        self._socket.send_multipart(msg.frames())

    def _send_gone(self):
        msg = pr.Message(pr.WORKER, pr.GONE, self.service)
        self._socket.send_multipart(msg.frames())

    def _send_hbeat(self):
        msg = pr.Message(pr.WORKER, pr.HBEAT, self.service)
        self._socket.send_multipart(msg.frames())

    def receive(self, timeout_sec : int = None) -> pr.Message:
        timeout = int(timeout_sec * 1000) if timeout_sec else None

        socks = dict(self._poller.poll(timeout=timeout))
        if socks.get(self._socket) == zmq.POLLIN:
            frames = self._socket.recv_multipart()
            msg = pr.parse(frames)
        else:
            print("Error! Timed out waiting for tasks from manager.")
            return

