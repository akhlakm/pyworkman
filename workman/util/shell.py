import os
import shlex
import subprocess

def execute_command(command : str, *, stdin : any = None,
                    capture : bool = True) -> subprocess.CompletedProcess:
    """
    Execute a shell command with arguments and optional stdin value.

    Args:
        stdin    any: Values to pipe to the stdin.
        capture bool: Whether to capture the stdout and stderr.

    Returns: subprocess.CompletedProcess
    """

    cmdlist = shlex.split(command)
    if stdin is not None:
        stdin = str(stdin)
        stdin = bytes(stdin, encoding='utf-8')
    result = subprocess.run(cmdlist, shell=False,
                            capture_output=capture, input=stdin)
    return result


def watch_stdout(command : str, char_chunk : int = 1000):
    """
    Execute a shell command with arguments and capture stdout and stderr
    in real time.

    Yields the output in a size of char_chunk.
    """

    cmdlist = shlex.split(command)
    process = subprocess.Popen(
        cmdlist, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    buffer = ""
    for line in process.stdout:
        buffer += line.decode()
        if len(buffer) >= char_chunk:
            yield buffer
            buffer = ""

    if len(buffer):
        yield buffer


def have_command(command : str, return_code : int = 0) -> bool:
    """
    Returns true if a command exists in shell.
    Args:
        return_code : Return code to check for success (0).
    """
    try:
        cmd = execute_command(command, capture=True)
        if return_code:
            return cmd.returncode == return_code
        else:
            return True
    except FileNotFoundError:
        return False


def install_pkg(pkg_name : str, requirements_file : str = None):
    """
    Make sure a python package with a specific version is installed.
    Returns true if pip install is successful.
    """

    # read the python requirements file if any.
    if requirements_file is None:
        if os.path.exists('requirements.txt'):
            requirements_file = 'requirements.txt'

    pkg_spec = None
    if requirements_file:
        # parse package name string
        print("Reading", requirements_file)
        with open(requirements_file) as fp:
            for line in fp:
                if pkg_name in re.split("[ =><@]+", line):
                    pkg_spec = line

    pkg_spec = pkg_spec if pkg_spec else pkg_name

    print("Installing", pkg_spec)
    cmd = execute_command(f"pip -v install -U {pkg_spec}", capture=False)
    return cmd.returncode == 0


def install_requirements(requirements_file : str = 'requirements.txt'):
    """ Runs pip install on a given requirements.txt file.
        Returns True if pip run is successful.
        Raises FileNotFoundError if the file is missing.
    """
    if os.path.exists(requirements_file):
        print("Installing", requirements_file)
        cmd = execute_command(
            f"pip -v install -U -r {requirements_file}", capture=False)
        return cmd.returncode == 0
    else:
        raise FileNotFoundError(requirements_file)
