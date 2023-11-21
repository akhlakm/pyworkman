# Run a simple echo service.
from util import conf
from workman.worker import Worker

with Worker(conf.WorkMan.mgr_url, 'echo', 'echo-worker') as worker:
    try:
        while True:
            msg = worker.receive()
            worker.update("Preparing response.")
            worker.reply(msg.message)
            worker.done()
    except KeyboardInterrupt:
        print("\nShutting down worker.")
