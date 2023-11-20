# Header bit
CLIENT    = b'C'
WORKER    = b'W'
MANAGER   = b'M'

# Action bit
READY   = b'\001'
REQUEST = b'\002'
HBEAT   = b'\003'
REPLY   = b'\004'
UPDATE  = b'\005'
ABORT   = b'\006'
DONE    = b'\007'
STATUS  = b'\008'

# Timing
ZMQ_LINGER = 2000
HBEAT_TIMEOUT = 10
HBEAT_INTERVAL = 2.5
WORKER_BUSY_TIMEOUT = 900

class Message(object):
    allowed_sender = (CLIENT, WORKER, MANAGER)
    allowed_action = {
        CLIENT: (REQUEST, STATUS, ABORT),
        WORKER: (READY, HBEAT, UPDATE, DONE),
        MANAGER: (REPLY, HBEAT, ABORT)
    }

    def __init__(self, sender, action, service, identifier, message = None,
                 address = None):
        if message is None:
            message = []

        if encode(sender) not in self.allowed_sender:
            raise ValueError("Invalid sender", sender)

        if encode(action) not in self.allowed_action[encode(sender)]:
            raise ValueError("Invalid action", action)

        self.address = address
        self.id = identifier
        self.sender = sender
        self.action = action
        self.service = service
        self.message = message

    def frames(self) -> list[bytes]:
        body = []
        if self.address:
            # Address needed for the router 
            body += [self.address]

        body += [
            b'',
            encode(self.sender),
            encode(self.action),
            encode(self.service),
            encode(self.id),
        ]
        body += [encode(m) for m in self.message]

        print("Payload:", body)
        return body
    
    def __repr__(self) -> str:
        items = [f"{k}: {v}"
                 for k, v in self.__dict__.items()
                 if not k.startswith("_")]
        return "Message: " +" ".join(items)

def parse(frames : list[bytes]) -> Message:
    print("Replied:", frames)
    assert len(frames) >= 5, "Invalid message, not enough frames"

    if frames[0] != b'':
        address = frames.pop(0)
    else:
        address = None

    assert frames.pop(0) == b'', "Invalid message, non-empty first frame"
    sender      = decode(frames[0])
    action      = decode(frames[1])
    service     = decode(frames[2])
    identifier  = decode(frames[3])
    message     = [decode(f) for f in frames[4:]]
    return Message(sender, action, service, identifier, message,
                   address=address)

def encode(s : str) -> bytes:
    if type(s) == bytes:
        return s
    return str(s).encode('utf-8')

def decode(b : bytes) -> str:
    if type(b) == str:
        return b
    return b.decode('utf-8', errors='ignore')
