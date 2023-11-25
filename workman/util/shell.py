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

def watch_stdout(command : str):
    cmdlist = shlex.split(command)
    process = subprocess.Popen(
        cmdlist, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in process.stdout:
        yield line

