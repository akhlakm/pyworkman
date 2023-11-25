import os
from workman.worker import Worker
from workman.util.shell import watch_stdout, ssh_tunnel
from workman.util.makeconf import Config, dataclass

@dataclass
class _shell:
    mgr_url : str = "tcp://127.0.0.1:5455"
    key_file : str = "mgr.key"
    svc_name : str = f"{os.uname().nodename}-Shell"
    ssh_conn_str : str = None

with Config('config-svc.yaml') as yaml:
    conf = yaml.section(_shell)

ssh_tunnel(conf.ssh_conn_str)

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
            for output in watch_stdout(payload.command):
                worker.update(output)

            worker.done("Command executed")

        except Exception as err:
            worker.done_with_error(str(err))

