#!/usr/bin/env python
from workman.worker import Send, StartWorker

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
        dict(help="Reverse the message.", default=False)

    @staticmethod
    def run(send : Send, job : 'EchoService'):
        send.update("Input: " + job.message)
        if job.reverse:
            send.reply(job.message[::-1])
        else:
            send.reply(job.message)

# -----------------------------------------------
StartWorker(EchoService, MGR, KEY)

# For testing, we can directly call the run function
# -----------------------------------------------
# test = EchoService()
# test.message = "hello world"
# test.reverse = True
# EchoService.run(Send, test)
