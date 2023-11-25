import os
import conf
from workman.worker import Worker
from workman.util import shell

svc_name = f"{os.uname().nodename}-Shell"

with Worker(conf.WorkMan.mgr_url, svc_name) as worker:
    worker.define("Shell executor",
        "Directly execute a terminal command. "
        "WARN! Be careful using this service!",
        command = dict(help="Required command to execute.", type=str),
    )

    while True:
        payload = worker.receive()
        print("Executing:", payload.job, "Input:", payload.command)

        buffer = ""
        for output in shell.watch_stdout(payload.command):
            outstr = output.decode()
            buffer += outstr
            print(outstr)

            if len(buffer) >= 1000:
                worker.update(buffer)
                buffer = ""

        if len(buffer):
            worker.update(buffer)
        worker.done("Command executed")
