""" Run a shell executor service under the current python environment.
    Create a ssh tunnel first, if required:
        workman tunnel
"""

import os
from workman.worker import Worker
from workman.util.shell import watch_stdout
from workman.util.makeconf import Config, dataclass


@dataclass
class _conf:
    mgr_url : str = "tcp://127.0.0.1:5455"
    key_file : str  = "/home/akhlak/mgr.key"
    svc_name : str = f"{os.uname().nodename}-Shell"

# Init config. Use with block to save to a yaml file.
conf = Config().section(_conf)


def execute(job : Worker, command):
    for output in watch_stdout(command):
        job.update(output)

    job.done("Command executed")


with Worker(conf.mgr_url, conf.svc_name, conf.key_file) as worker:
    worker.define("Shell executor",
        "Directly execute a terminal command. "
        "WARN! Be careful using this service!",
        command = dict(help="Required command to execute.", type=str),
    )

    while True:
        payload = worker.receive()
        print("Running job:", payload.job)

        try:
            execute(worker, payload.command)
        except Exception as err:
            worker.done_with_error(str(err))

