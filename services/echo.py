""" Run a simple echo service. """
import time
from . import conf
from workman.worker import Worker


def start(name = None):
    name = name if name else 'echo-worker'
    with Worker(conf.WorkMan.mgr_url, 'echo', name) as service:
        service.define("Echo Test",
            "Echo the sent message",
            message = dict(help="Required message to send", type=str),
            name = dict(default="world", help="Optional name"),
        )
        while True: execute(service)


def execute(worker : Worker):
    payload = worker.receive()
    print("Executing:", payload.job, "Input:", payload.message)

    worker.update(f"Hello {payload.name}! Generating response.")
    print("Update 1")
    time.sleep(2)

    worker.update("60% complete.")
    print("Update 2")
    time.sleep(4)

    worker.update("Almost done.")
    print("Update 3")
    time.sleep(4)

    worker.reply(payload.message)
    print("Done:", payload.job, "Replied:", payload.message)
    worker.done()


if __name__ == '__main__':
    start()
