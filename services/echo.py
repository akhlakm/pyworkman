# Run a simple echo service.
import time
from util import conf
from workman.worker import Worker

with Worker(conf.WorkMan.mgr_url, 'echo', 'echo-worker') as worker:
    try:
        while True:
            msg = worker.receive()
            print("Executing:", msg.job, "Input:", msg.message)

            worker.update("Preparing response.")
            print("Update 1")
            time.sleep(2)

            worker.update("Almost done.")
            print("Update 2")
            time.sleep(4)

            worker.update("95% complete.")
            print("Update 3")
            time.sleep(4)

            worker.reply(msg.message)
            print("Done:", msg.job, "Replied:", msg.message)
            worker.done()

    except KeyboardInterrupt:
        print("\nShutting down worker.")
