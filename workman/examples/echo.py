#!/usr/bin/env python
from workman.worker import Worker, StartWorker

MGR = "tcp://127.0.0.1:5455"    # Setup SSH tunnel: workman tunnel
KEY = "mgr.key"                 # Download from MGR.

class EchoService:
    """
A simple echo service for test purposes.

This service can be run with the StartWorker() function.
Input fields are defined by non-callable class properties.
Properties starting with _ are ignored.

When a job request is received, the staticmethod "run()" will be called
with the Worker handler and job inputs.
    """

    message : str = \
        dict(help="Message to send.", default="hello", required=1)
    
    reverse : bool = \
        dict(help="Reverse the message.", default=False, choices=[True, False])

    @staticmethod
    def run(worker : Worker, fields : 'EchoService'):
        print(fields.message)
        if fields.reverse:
            worker.reply(fields.message[::-1])
        else:
            worker.reply(fields.message)


# -----------------------------------------------
StartWorker(EchoService, MGR, KEY)
