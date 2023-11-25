import sys
from workman import conf

def usage():
    print("USAGE:")
    print("\tworkman mgr|ui|update|copy")
    print("\tworkman copy <example name>")
    sys.exit(1)


def main():
    if len(sys.argv) <= 1:
        conf._c.save_yaml()
        usage()

    cmd = sys.argv[1]

    if cmd == "mgr":
        from workman import broker
        broker.start()

    elif cmd == "ui":
        from workman import backend
        backend.start()

    elif cmd == "update":
        # Reinstall pyworkman.
        from workman.util import shell
        repo = "git+ssh://git@github.com/akhlakm/pyworkman.git"
        shell.execute_command(f"pip install -U {repo}", capture=False)

    elif cmd == "copy":
        # Copy an example to current directory.
        import os, shutil
        if len(sys.argv) < 3:
            usage()
        name = sys.argv[2]
        shutil.copyfile(f"{os.path.dirname(__file__)}/examples/{name}.py",
                        f"./pywm-{name}.py")
        print("Copy OK:", name)

    else:
        usage()
