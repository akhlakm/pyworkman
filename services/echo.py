# Run a simple echo service.
import time
from util import conf
from workman.worker import Worker

with Worker(conf.WorkMan.mgr_url, 'echo', 'echo-worker') as worker:
    try:
        while True:
            msg = worker.receive()
            worker.update("Preparing response.")
            time.sleep(2)

            worker.update("Almost done.")
            time.sleep(4)

            worker.update("95% complete.")
            time.sleep(4)

            worker.reply(msg.message)
            worker.done()
            
    except KeyboardInterrupt:
        print("\nShutting down worker.")
