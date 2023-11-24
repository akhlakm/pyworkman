import sys
from workman import broker, backend

def usage():
    print("USAGE:")
    print("\tworkman mgr|ui|<service.package> [<worker name>]")
    print("\nExamples:")
    print("\tworkman ui")
    print("\tworkman mgr")
    print("\tworkman service.echo")
    print("\tworkman service.echo worker1")
    sys.exit(1)

def import_from(module, func):
    module = __import__(module, fromlist=[func])
    return getattr(module, func)

def main():
    if len(sys.argv) <= 1:
        usage()

    cmd = sys.argv[1]

    if cmd == "mgr":
        broker.start()

    elif cmd == "ui":
        backend.start()

    else:
        # workman service.echo worker1
        svcname = cmd
        if len(sys.argv) > 2:
            worker = sys.argv[2]
        else:
            worker = None

        try:
            start = import_from(svcname, func="start")
            print(f"Import OK: {svcname}.start")
        except:
            usage()

        start(worker)
