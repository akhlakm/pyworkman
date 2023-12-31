import zmq
import time
import random
import signal
import argparse
from collections import namedtuple
from workman import protocol as pr


class ServiceWorker(object):
    def __init__(self, manager_url, service, key_file : str = "mgr.key"):
        self.service = service
        self.manager_url = manager_url
        self.definition = None
        self._zmq_context = zmq.Context.instance()
        self.identity : bytes = pr.createId(pr.WORKER)
        self._socket : zmq.Socket = None
        self._poller : zmq.Poller = None
        self._abort = False
        self._jobid = None
        self._is_busy = False
        self._key_file = key_file
        self._hb_timeout = pr.HBEAT_TIMEOUT
        self._hb_interval = pr.HBEAT_INTERVAL
        self._last_sent = time.time()
        self._last_received = time.time()
        self._timer = None

    def _is_connected(self):
        return self._socket is not None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    def _init_encryption(self):
        keys = open(self._key_file).read().strip().encode("utf-8").split(b"\n")
        random.shuffle(keys)
        pr.Encryptor = pr.encryptor(*keys)

    def _start_timer(self):
        self._timer = time.time()

    def _elapsed(self) -> str:
        """ Return elapsed time string."""
        if self._timer:
            return f"{(time.time() - self._timer):.3f} s"
        else:
            return "0 s"

    def abort(self) -> bool:
        return self._abort

    def connect(self, reconnect=False):
        if reconnect:
            self.close()
        if self._is_connected():
            return

        print(f"Connecting to {self.manager_url}")
        self._init_encryption()
        self._socket = self._zmq_context.socket(zmq.DEALER)
        self._socket.setsockopt(zmq.LINGER, pr.ZMQ_LINGER)
        self._socket.setsockopt(zmq.IDENTITY, self.identity)
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

    def _send(self, action, job = None, message = None):
        msg = pr.Message(action, self.service, job, message)
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
    
    def _make_bool(self, boolean) -> bool:
        return str(boolean).lower() in [
            "true", "1", "yes", "y", "yeah", "yep", "t", "of course"]
    
    def define(self, svcName : str, svcDesc : str, **fields):
        """ Define the payload json.
            >>> worker.define("Echo Service", "Echo the sent message",
                    message = dict(help="Required message", type=str),
                    name = dict(default="world", help="Optional name"),
                )
        """
        for field, obj in fields.items():
            assert type(obj) == dict, f"Dict required for {field} definition"

            # must specify a help string
            assert "help" in obj, f"Help string required in {field} field"

            # if no default specified, it is a required field.
            if not "default" in obj: obj["required"] = 1

            if not "type" in obj:
                # determine the type from the default value.
                assert "default" in obj and obj["default"] is not None, \
                    f"Type must be set for field {field}"
                obj['type'] = type(obj["default"]).__name__

            elif type(obj["type"]) != str:
                # use the name of the callable
                obj['type'] = obj['type'].__name__

            if "choices" in obj:
                # must be a list
                assert type(obj["choices"]) in [list, tuple], \
                    f"choices must be a list or tuple in field {field}"
                # default must be one of the choices
                assert "default" not in obj \
                    or obj["default"] in obj["choices"], \
                    f"Default must be one of the choices in field {field}"

            if obj['type'] == 'bool' and 'choices' not in obj:
                obj['choices'] = ['Yes', 'No']
                # Convert default to Yes, No
                if 'default' in obj:
                    if self._make_bool(obj['default']):
                        obj['default'] = 'Yes'
                    else:
                        obj['default'] = 'No'

        self.definition = {
            "name": svcName, "desc": svcDesc, "fields": fields
        }
        self._send_ready()
        print(f"{pr.decode(self.identity)} ready for '{self.service}' jobs.")


    def _parse_payload(self, msg : pr.Message) -> namedtuple:
        """
        Try to parse the payload according to the definition.
        Return: A namedtuple of the payload. None on error.
        """
        assert self.definition, "Payload definition not set, define() first"
        payload = pr.unserialize(msg.message)
        if not type(payload) == dict:
            self.done_with_error(
                f"Invalid payload type: '{type(payload)}', dict expected.")
            return None
        else:
            service = self.definition["name"]
            fields = self.definition["fields"]
            for name, field in fields.items():
                if name not in payload:
                    if "required" in field and field['required']:
                        self.done_with_error(f"Field {name} is required")
                        return None
                    elif "default" in field:
                        # assign the default one.
                        payload[name] = field["default"]

                if "choices" in field and payload[name] not in field["choices"]:
                    self.done_with_error(
                        f"Invalid choice for {name}: '{payload[name]}'")
                    return None

                # Convert to python bool
                if field["type"] == "bool":
                    payload[name] = self._make_bool(payload[name])

                elif field["type"] == "int":
                    try:
                        payload[name] = int(payload[name])
                    except Exception as err:
                        self.done_with_error(
                            f"Invalid int {name}: '{payload[name]}' ({err})")
                        return None

                elif field["type"] == "float":
                    try:
                        payload[name] = float(payload[name])
                    except Exception as err:
                        self.done_with_error(
                            f"Invalid float {name}: '{payload[name]}' ({err})")
                        return None

            payload["job"] = msg.job
            defn = namedtuple("Job", [k for k in payload.keys()])
            return defn(**payload)

    def reply(self, message : str):
        assert self._is_busy, "Cannot reply after done"
        self._send(pr.REPLY, self._jobid, message)

    def update(self, message : str):
        assert self._is_busy, "Cannot update after done"
        self._send(pr.UPDATE, self._jobid, message)

    def done(self, reply : str = None):
        assert self._is_busy, "Cannot send done twice"
        if reply: self.reply(reply)
        self.update(f"Job Duration: {self._elapsed()}")
        self._send(pr.DONE, self._jobid)
        self._is_busy = False
        self._timer = None

    def done_with_error(self, error_message : str):
        print(error_message)
        self.done(f"FATAL: {error_message}")

    def send_hbeat(self):
        ds = time.time() - self._last_sent
        dr = time.time() - self._last_received
        if ds > self._hb_interval:
            self._send(pr.HBEAT)

    def receive(self) -> namedtuple:
        """ Waits forever to receive a single request.
            Returns the received payload object parsed using definition.
        """
        msg = None

        assert self.definition, "Payload definition not set, call define()"

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
                    self._send_ready()

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
                # parse with definition or reply with error.
                payload = self._parse_payload(msg)
                if payload:
                    self._start_timer()
                    return payload


class Send:
    """ An interface to send message over the network.
        Useful for testing purposes.
    """
    worker : ServiceWorker = None

    @staticmethod
    def update(*msg : any):
        message = " ".join([str(m) for m in msg])
        print("-- Update:", message, flush=True)
        if Send.worker:
            Send.worker.update(message)
    
    @staticmethod
    def reply(*msg : any):
        message = " ".join([str(m) for m in msg])
        print("--- Reply:", message, flush=True)
        if Send.worker:
            Send.worker.reply(message)


def start_worker(service : type, mgr_url, key_file):
    """ Start a worker for the service.
        Keeps running indefinitely, exits when shutdown requested.
    """

    # Use the class name as service name.
    try: svcName = service._name
    except AttributeError:
        svcName = service.__name__

    # The service must define a run function to process a job and payload.
    assert hasattr(service, "run") and callable(service.run), \
        f"{svcName} must define run(send : Send, job : {svcName}) staticmethod"

    # Fallback to docstring if not defined.
    try: svcDesc = service._desc
    except AttributeError:
        svcDesc = service.__doc__

    # All arguments not starting with _ are payload fields.
    fields = {
        k : v for k, v in service.__dict__.items()
        if not k.startswith("_") and not callable(v)
    }

    # Create commandline argument parser
    cmdline = argparse.ArgumentParser(prog=svcName, description=svcDesc)
    cmdline.add_argument("--pywm", default=False, action='store_true',
                            help="Run as a pyworkman service worker.")

    # Make sure the fields are valid.
    for k, v in fields.items():
        assert type(v) == dict, f"Field {k} must be a dictionary."
        cmdline.add_argument('--' + k, choices=v.get('choices'),
            default=v.get('default'), help=v.get('help'), type=v.get('type'))

    args = cmdline.parse_args()

    # Handle termination
    shutdown = False
    def _sig_handler(sig, _):
        global shutdown
        shutdown = True
        raise RuntimeError("Shutdown signal received.")

    signal.signal(signal.SIGINT, _sig_handler)
    signal.signal(signal.SIGTERM, _sig_handler)

    # if --pywm not specified, do not start the worker.
    if not args.pywm:
        return service.run(args, Send)

    # Start the worker.
    with ServiceWorker(mgr_url, svcName, key_file) as worker:
        Send.worker = worker
        worker.define(svcName, svcDesc, **fields)

        while not shutdown:
            payload = worker.receive()
            print("\nRunning job:", payload.job)

            try:
                reply = service.run(payload, Send)
                worker.done(str(reply))
            except Exception as err:
                print(err)
                worker.done_with_error(str(err))

            print("Job done:", payload.job)
