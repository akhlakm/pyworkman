import sys
from workman import conf, broker, backend

def usage():
    print("USAGE:")
    print("\tworkman mgr|ui")
    sys.exit(1)


def main():
    conf._c.save_yaml()

    if len(sys.argv) <= 1:
        usage()

    cmd = sys.argv[1]

    if cmd == "mgr":
        broker.start()

    elif cmd == "ui":
        backend.start()

    else:
        usage()
