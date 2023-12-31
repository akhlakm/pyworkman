import json
import time
from workman import conf
from cryptography.fernet import Fernet, MultiFernet

# Sender bit
CLIENT    = b'C'
WORKER    = b'W'

# Action bit
ABORT   = b'A'
HBEAT   = b'B'
DONE    = b'D'
GONE    = b'G'
LIST    = b'L'
REPLY   = b'P'
REQUEST = b'Q'
READY   = b'R'
STATUS  = b'S'
UPDATE  = b'U'

# Timing
ZMQ_LINGER          = 2000  # msec
HBEAT_TIMEOUT       = 600   # sec
HBEAT_INTERVAL      = 60    # sec

Encryptor = None

def encryption_key():
    return Fernet.generate_key()

def encryptor(*keys : bytes):
    if conf.WorkMan.enable_encryption:
        return MultiFernet([Fernet(key) for key in keys])
    else:
        # Return None to disable encryption.
        return None
    
def createId(sender) -> bytes:
    assert sender in [CLIENT, WORKER]
    s = str(time.time()).split(".")[1]
    return sender + encode(s)

class Message(object):
    def __init__(self, action : bytes, service : str = "", job : str = "",
                 message : str = ""):

        assert type(action) == bytes, "Action must be bytes"

        self.identity : bytes = None
        self.action : bytes = action
        self.service : str = service
        self.job : str = job
        self.message : str = message

    def set_identity(self, iden : bytes):
        self.identity = iden

    def frames(self) -> list[bytes]:
        """ Create a payload for sending via socket. """
        if self.identity:
            # identity needed for the router
            body = [self.identity, b'', encrypt(self.service)]
        else:
            body = [b'', encrypt(self.service)]

        if self.message:
            body.append(self.action)
            body.append(encrypt(self.job))
            body.append(encrypt(self.message))
        elif self.job:
            body.append(self.action)
            body.append(encrypt(self.job))
        elif self.action != HBEAT:
            body.append(self.action)

        if conf.WorkMan.trace_packets:
            print("--  Sending:", body)
        return body

    @classmethod
    def parse(cls, frames : list[bytes]):
        """ Parse a payload received via socket. """

        if conf.WorkMan.trace_packets:
            print("-- Received:", frames)

        assert len(frames) >= 2, "Invalid message, not enough frames"

        if frames[0] != b'':
            identity = frames.pop(0)
        else:
            identity = None

        assert frames.pop(0) == b'', "Invalid message, non-empty first frame"
        service     = decrypt(frames[0])
        action      = frames[1] if len(frames) > 1 else HBEAT
        job         = decrypt(frames[2]) if len(frames) > 2 else ""
        message     = decrypt(frames[3]) if len(frames) > 3 else ""

        msg = cls(action, service, job, message)
        msg.set_identity(identity)
        return msg

    @staticmethod
    def actions() -> dict:
        """ Nicely formatted names for the actions. """
        return {
            "ready" : READY,
            "request" : REQUEST,
            "heartbeat" : HBEAT,
            "reply" : REPLY,
            "update" : UPDATE,
            "abort" : ABORT,
            "done" : DONE,
            "status" : STATUS,
            "disconnect": GONE,
        }

    def items(self) -> dict:
        action = decode(self.action)
        for k, v in Message.actions().items():
            if v == self.action:
                action = k
        items = {
            'identity': decode(self.identity),
            'action': action,
            'service': self.service,
            'job': self.job,
            'message': self.message,
        }
        return items
    
    def __repr__(self) -> str:
        return f"Message({str(self.items())})"


def encode(s : str) -> bytes:
    if s is None:
        return b""
    if type(s) == bytes:
        return s
    return str(s).encode('utf-8')

def decode(b : bytes) -> str:
    if b is None:
        return ""
    if type(b) == str:
        return b
    return b.decode('utf-8', errors='ignore')

def encrypt(s : str) -> bytes:
    b = encode(s)
    if Encryptor: b = Encryptor.encrypt(b)
    return b

def decrypt(b : bytes) -> str:
    assert type(b) == bytes
    if Encryptor: b = Encryptor.decrypt(b)
    return decode(b)

def serialize(items : dict) -> str:
    class JSONSerializer(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (bytes, bytearray)):
                return decode(obj)
            return json.JSONEncoder.default(self, obj)
    return json.dumps(items, cls=JSONSerializer)

def unserialize(message : str) -> dict:
    return json.loads(message)