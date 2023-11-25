""" Run a simple echo service for workman. """
import time
import conf
from workman.worker import Worker

def start():
    """ Start the worker listening for job requests.
    """
    with Worker(conf.WorkMan.mgr_url, 'echo') as service:
        # define the input fields for a job.
        service.define("Echo Test",
            "Echo the sent message",
            message = dict(help="Required message to send", type=str),
            name = dict(default="world", help="Optional name"),
        )
        # listen forever
        while True: execute(service)


def execute(worker : Worker):
    """ Wait and execute a single job request.
    """
    payload = worker.receive()
    print("Executing:", payload.job, "Input:", payload.message)

    worker.update(f"Hello {payload.name}! Generating response.")
    print("Update 1 sent")
    time.sleep(2)

    worker.update("60% complete.")
    print("Update 2 sent")
    time.sleep(4)

    worker.update("Almost done.")
    print("Update 3 sent")
    time.sleep(4)

    worker.reply(payload.message)
    print("Done:", payload.job, "Replied:", payload.message)
    worker.done()


if __name__ == '__main__':
    start()
