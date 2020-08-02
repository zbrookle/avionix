from logging import info, error
from subprocess import STDOUT, check_output, CalledProcessError


def custom_check_output(command: str):
    info(f"Running command: {command}")
    try:
        output = check_output(command.split(" "), stderr=STDOUT).decode("utf-8")
    except CalledProcessError as err:
        error(err.output.decode("utf-8"))
        raise err
    info(f"Output from command:\n{output}")
    return output
