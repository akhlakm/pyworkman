"""
    Run a shell executor service with optional ssh tunnel setup.
    As SSH connection may require a password,
        first set the connection string and run once to create the tunnel.
    Then set the connection string to None to start the service using nohup.
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


def execute(job : Worker):
    payload = job.receive()
    print("Running job:", payload.job)
    try:
        for output in watch_stdout(payload.command):
            job.update(output)

        job.done("Command executed")

    except Exception as err:
        job.done_with_error(str(err))


with Worker(conf.mgr_url, conf.svc_name, conf.key_file) as worker:
    worker.define("Shell executor",
        "Directly execute a terminal command. "
        "WARN! Be careful using this service!",
        command = dict(help="Required command to execute.", type=str),
    )
    print("Please create a ssh tunnel if required.")
    print("\tworkman tunnel")

    while True:
        execute(worker)
