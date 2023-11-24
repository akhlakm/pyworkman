import sys
from workman import conf

def usage():
    print("USAGE:")
    print("\tworkman mgr|ui|update")
    print("\tworkman tunnel [<localport=5455> <remoteport=5455>]")
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
        if len(sys.argv) == 4:
            # Usage: workman tunnel <localport> <remoteport>
            lp = sys.argv[2]
            rp = sys.argv[3]
        else:
            lp = 5455
            rp = 5455

        tunnel = f"-N -f -L 127.0.0.1:{lp}:127.0.0.1:{rp}"
        sshcmd = f"ssh {tunnel} {conf.WorkMan.ssh_conn_string}"
        input(sshcmd)
        shell.execute_command(sshcmd, capture=False)
    else:
        usage()
