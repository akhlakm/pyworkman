# Header bit
CLIENT    = b'C'
WORKER    = b'W'
MANAGER   = b'M'

# Action bit
READY   = b'\x001'
REQUEST = b'\x002'
HBEAT   = b'\x003'
REPLY   = b'\x004'
UPDATE  = b'\x005'
ABORT   = b'\x006'
DONE    = b'\x007'
STATUS  = b'\x008'
GONE    = b'\x009'

# Timing
ZMQ_LINGER = 2000
HBEAT_TIMEOUT = 60
HBEAT_INTERVAL = 10
WORKER_BUSY_TIMEOUT = 900


class Message(object):
    allowed_sender = (CLIENT, WORKER, MANAGER)
    allowed_action = {
        CLIENT: (REQUEST, STATUS, ABORT),
        MANAGER: (REPLY, HBEAT, REQUEST, ABORT),
        WORKER: (READY, HBEAT, UPDATE, DONE, GONE, REPLY),
    }

    def __init__(self, sender, action, service, job = None, message = None):
        if message is None:
            message = []

        sender = encode(sender)
        action = encode(action)

        if sender not in self.allowed_sender:
            raise ValueError("Invalid sender", sender)

        if action not in self.allowed_action[sender]:
            raise ValueError("Invalid action", action)

        self.identity : bytes = None
        self.sender : bytes = sender
        self.action : bytes = action
        self.service : str = service
        self.job : str = job
        self.message : str = message

    def set_identity(self, iden : bytes):
        self.identity = iden

    def frames(self) -> list[bytes]:
        """ Create a payload for sending via socket. """
        body = []
        if self.identity:
            # identity needed for the router 
            body += [self.identity]

        body += [
            b'',
            self.sender,
            self.action,
            encode(self.service),
            encode(self.job),
        ]
        body += [encode(m) for m in self.message]

        print("Message:", body)
        return body

    @classmethod
    def parse(cls, frames : list[bytes]):
        """ Parse a payload received via socket. """

        print("Replied:", frames)
        assert len(frames) >= 5, "Invalid message, not enough frames"

        if frames[0] != b'':
            identity = frames.pop(0)
        else:
            identity = None

        assert frames.pop(0) == b'', "Invalid message, non-empty first frame"
        sender      = frames[0]
        action      = frames[1]
        service     = decode(frames[2])
        job         = decode(frames[3])
        message     = [decode(f) for f in frames[4:]]

        msg = cls(sender, action, service, job, message)
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
            'sender': decode(self.sender),
            'action': action,
            'service': self.service,
            'job': self.job,
            'message': " ".join(self.message),
        }
        return items
    
    def __repr__(self) -> str:
        return f"Message({str(self.items())})"



def encode(s : str) -> bytes:
    if type(s) == bytes:
        return s
    return str(s).encode('utf-8')

def decode(b : bytes) -> str:
    if type(b) == str:
        return b
    return b.decode('utf-8', errors='ignore')
