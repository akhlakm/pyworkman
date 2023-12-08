#!/usr/bin/env python
import os
from workman.worker import start_worker, Send
from workman.util import shell

MGR = "tcp://127.0.0.1:5455"    # Setup SSH tunnel: workman tunnel
KEY = "mgr.key"                 # Download from MGR.

class PyWMService:
    """
    Directly execute a terminal command.
    WARN! Be careful using this service!
    """
    _name = 'Shell:'+os.uname().nodename

    command : str = \
        dict(help="Command to execute.", default="conda info", required=1)
    
    @staticmethod
    def run(send : Send, job : 'PyWMService'):
        for output in shell.watch_stdout(job.command):
            send.update(output)

# Specify --pywm to start as a service worker
# ----------------------------------------------
start_worker(PyWMService, MGR, KEY)
