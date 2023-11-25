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


def ssh_tunnel(conn_string : str = None):
    """
    Create a SSH tunnel using a connection string formatted as
    <localport>#user@host.com:22#<remoteport>.

    Returns: On success or None connection string.
    Raises: ConnectionError on failure.
    """
    if conn_string:
        lp, user, rp = conn_string.split("#")
        sshcmd = f"ssh -N -f -L {lp}:127.0.0.1:{rp} {user}"
        result = execute_command(sshcmd)
        if result.returncode:
            raise ConnectionError(result.stdout + result.stderr)
