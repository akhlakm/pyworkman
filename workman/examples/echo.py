#!/usr/bin/env python
from workman.worker import Worker, StartWorker

MGR = "tcp://127.0.0.1:5455"    # Setup SSH tunnel: `workman tunnel`
KEY = "mgr.key"                 # Download from MGR.

class EchoService:
    """ A simple echo service for test purposes. """
    message : str = \
        dict(help="Message to send.", default="hello", required=1)

    @staticmethod
    def run(worker : Worker, fields : 'EchoService'):
        print(fields.message)
        worker.reply(fields.message)


# -----------------------------------------------
StartWorker(EchoService, MGR, KEY)
