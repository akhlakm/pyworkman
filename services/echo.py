# Run a simple echo service.
import time
import conf
from workman.worker import Worker

with Worker(conf.WorkMan.mgr_url, 'echo', 'echo-worker') as worker:
    worker.define(
        "Echo Service",
        "Echo the sent message",
        message = dict(help="Required message to send", type=str),
        name = dict(default="world", help="Optional name"),
    )
    try:
        while True:
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

    except KeyboardInterrupt:
        print("\nShutting down worker.")
