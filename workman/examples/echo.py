#!/usr/bin/env python
from workman.worker import start_worker

class EchoService:
    """
A simple echo service for test purposes.

This service can be run with the start_worker() function.
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
    def run(job : 'EchoService', send):
        send.update("Input: " + job.message)
        if job.reverse:
            send.reply(job.message[::-1])
        else:
            send.reply(job.message)

# Specify --pywm to start as a service worker
# ----------------------------------------------
if __name__ == '__main__':
    MGR = "tcp://127.0.0.1:5455"    # Setup SSH tunnel: workman tunnel
    KEY = "mgr.key"                 # Download from MGR.
    start_worker(EchoService, MGR, KEY)
