import sys
from workman import conf

def usage():
    print("USAGE:")
    print("\tworkman mgr|ui|update")
    sys.exit(1)


def main():
    conf._c.save_yaml()

    if len(sys.argv) <= 1:
        usage()

    cmd = sys.argv[1]

    if cmd == "mgr":
        from workman import broker
        broker.start()

    elif cmd == "ui":
        from workman import backend
        backend.start()

    elif cmd == "update":
        from workman.util import shell
        shell.execute_command("pip install -U pyworkman", capture=False)

    else:
        usage()
