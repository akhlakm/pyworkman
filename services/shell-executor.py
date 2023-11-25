import os
from dataclasses import dataclass
from workman.worker import Worker
from workman.util.shell import watch_stdout
from workman.util.makeconf import Config

@dataclass
class _shell:
    mgr_url : str = "tcp://127.0.0.1:5455"
    key_file : str = "mgr.key"

c = Config("config-svc.yaml")
conf = c.section(_shell)
c.save_yaml()

svc_name = f"{os.uname().nodename}-Shell"

with Worker(conf.mgr_url, svc_name, conf.key_file) as worker:
    worker.define("Shell executor",
        "Directly execute a terminal command. "
        "WARN! Be careful using this service!",
        command = dict(help="Required command to execute.", type=str),
    )

    while True:
        payload = worker.receive()
        try:
            for output in watch_stdout(payload.command):
                worker.update(output)

            worker.done("Command executed")

        except Exception as err:
            worker.done_with_error(str(err))

