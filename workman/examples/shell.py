#!/usr/bin/env python
import os
from workman.worker import start_worker
from workman.util import shell

class PyWMService:
    """
    Directly execute a terminal command.
    WARN! Be careful using this service!
    """
    _name = 'Shell:'+os.uname().nodename

    command : str = \
        dict(help="Command to execute.", default="conda info", required=1)
    
    @staticmethod
    def run(job : 'PyWMService', send):
        for output in shell.watch_stdout(job.command):
            send.update(output)

# Specify --pywm to start as a service worker.
# ----------------------------------------------
if __name__ == '__main__':
    MGR = "tcp://127.0.0.1:5455"            # Setup SSH tunnel: workman tunnel
    KEY = os.path.expanduser("~/mgr.key")   # Download from MGR.
    start_worker(PyWMService, MGR, KEY)
