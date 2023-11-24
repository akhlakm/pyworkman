import sys
from workman import broker, backend

def usage():
    print("USAGE:")
    print("\tworkman mgr|ui")
    sys.exit(1)


def main():
    if len(sys.argv) <= 1:
        usage()

    cmd = sys.argv[1]

    if cmd == "mgr":
        broker.start()

    elif cmd == "ui":
        backend.start()

    else:
        usage()
