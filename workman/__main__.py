import sys
from workman import conf

def usage():
    print("USAGE:")
    print("\tworkman mgr|ui|update|tunnel")
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
        # Update the python packages.
        from workman.util import shell
        shell.execute_command("pip install -U pyworkman", capture=False)

    elif cmd == "tunnel":
        # Create ssh tunnel defined by the config.
        from workman.util import shell
        if len(sys.argv) < 4:
            print("USAGE:")
            print("\tworkman tunnel <localport> <remoteport>")
            sys.exit(1)

        lp = sys.argv[2]
        rp = sys.argv[3]
        tunnel = f"-N -f -L 127.0.0.1:{lp}:127.0.0.1:{rp}"

        shell.execute_command(
            f"ssh {tunnel} {conf.WorkMan.ssh_conn_string}", capture=False)
    else:
        usage()
