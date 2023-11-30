#!/usr/bin/env python
from workman.worker import start_worker, Send
from workman.util import shell

MGR = "tcp://127.0.0.1:5455"    # Setup SSH tunnel: workman tunnel
KEY = "mgr.key"                 # Download from MGR.

class ShellService:
    """
    Directly execute a terminal command.
    WARN! Be careful using this service!
    """

    command : str = \
        dict(help="Command to execute.", default="conda info", required=1)
    
    @staticmethod
    def run(send : Send, job : 'ShellService'):
        for output in shell.watch_stdout(job.command):
            send.update(output)

# -----------------------------------------------
start_worker(ShellService, MGR, KEY)

# For testing, we can directly call the run function.
# Comment the start_worker call to run the tests below.
# -----------------------------------------------------
test = ShellService()
test.command = "bash -i -c 'echo $PWD'"
ShellService.run(Send, test)
