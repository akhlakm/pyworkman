import zmq
import time
from workman import protocol as pr


class Worker(object):
    def __init__(self, manager_url, service, workerid, context=None):
        self.identity = workerid
        self.service = service
        self.manager_url = manager_url
        self.definition = {}
        self._zmq_context = context if context else zmq.Context.instance()
        self._socket : zmq.Socket = None
        self._poller : zmq.Poller = None
        self._abort = False
        self._jobid = None
        self._is_busy = False
        self._hb_timeout = pr.HBEAT_TIMEOUT
        self._hb_interval = pr.HBEAT_INTERVAL
        self._last_sent = time.time()
        self._last_received = time.time()

    def _is_connected(self):
        return self._socket is not None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    def abort(self) -> bool:
        return self._abort

    def connect(self, reconnect=False):
        if reconnect:
            self.close()
        if self._is_connected():
            return
        
        self._socket = self._zmq_context.socket(zmq.DEALER)
        self._socket.setsockopt(zmq.LINGER, pr.ZMQ_LINGER)
        self._socket.setsockopt(zmq.IDENTITY, pr.encode(self.identity))
        self._socket.connect(self.manager_url)
        self._stop = False

        self._poller = zmq.Poller()
        self._poller.register(self._socket, zmq.POLLIN)

    def close(self):
        if not self._is_connected():
            return
        self._send_gone()
        self._socket.setsockopt(zmq.LINGER, 0)
        self._poller.unregister(self._socket)
        self._socket.disconnect(self.manager_url)
        self._socket.close()
        self._socket = None

    def _send(self, action, job = None, message = None, identity = None):
        msg = pr.Message(pr.WORKER, action, self.service, job, message)
        if identity:
            msg.set_identity(identity)
        self._last_sent = time.time()
        self._socket.send_multipart(msg.frames())

    def _send_ready(self):
        self._is_busy = False
        self._jobid = None
        self._send(pr.READY, message=pr.serialize(self.definition))

    def _send_gone(self):
        self._send(pr.GONE)

    def _get_poll_timeout(self) -> int:
        """Return the poll timeout for the current iteration in milliseconds
        """
        wait = self._hb_interval + self._last_sent - time.time() # sec
        return max(0, int(1000 * wait))
    
    def define(self, **kwargs):
        """ Define the payload json. """
        for key in ["name", "desc", "fields"]:
            assert key in kwargs, f"{key} required"
        assert type(kwargs['fields']) == dict
        for field, obj in kwargs['fields'].items():
            for key in ["value", "type", "help"]:
                assert key in obj, f"{key} required in {field} field"
        self.definition = kwargs
        self._send_ready()

    def reply(self, message : str):
        self._send(pr.REPLY, self._jobid, message)

    def update(self, message : str):
        self._send(pr.UPDATE, self._jobid, message)

    def done(self):
        self._is_busy = False
        self._send(pr.DONE, self._jobid)

    def send_hbeat(self):
        if (time.time() - self._last_sent) > self._hb_interval:
            self._send(pr.HBEAT)

    def receive(self) -> pr.Message:
        """ Waits forever to receive a single request.
            Returns the received message object.
        """
        msg = None

        if not self._is_connected():
            raise RuntimeError("Not connected")
        
        while True:
            self.send_hbeat()

            try:
                timeout = self._get_poll_timeout()
                socks = dict(self._poller.poll(timeout=timeout))
            except zmq.error.ZMQError:
                if not self._is_connected():
                    print("Disconnected.")
                    continue
                else: raise

            if socks.get(self._socket) == zmq.POLLIN:
                msg = pr.Message.parse(self._socket.recv_multipart())
            else:
                # Timed out
                if (time.time() - self._last_received) > self._hb_timeout:
                    print("Mgr might be disconnected. Reconnecting.")
                    self.connect(reconnect=True)

                continue

            self._last_received = time.time()

            # Handle messages.
            if msg.action == pr.HBEAT:
                print(".", end="", flush=True)
            elif msg.action == pr.ABORT:
                self._abort = True
            elif msg.action == pr.READY:
                self._send(pr.READY, message=pr.serialize(self.definition))
            elif msg.action == pr.REQUEST:
                self._abort = False
                self._is_busy = True
                self._jobid = msg.job
                return msg


if __name__ == '__main__':
    # Run a simple echo service.
    from util import conf

    with Worker(conf.WorkMan.mgr_url, 'echo', 'worker-1') as worker:
        worker.define(
            name="Echo Service",
            desc="Echo the sent message",
            fields = {
                'value': dict(
                    value="hello", type="string", help="Value to send",
                    required=1
                )
            }
        )

        try:
            while True:
                msg = worker.receive()
                worker.update("Preparing response.")
                worker.reply(msg.message)
                worker.done()
        except KeyboardInterrupt:
            print("\nShutting down worker.")
