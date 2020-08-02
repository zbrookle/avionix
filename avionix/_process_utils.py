from subprocess import check_output, STDOUT
from logging import info


def custom_check_output(command: str):
    info(f"Running command: {command}")
    output = check_output(command.split(" "), stderr=STDOUT).decode("utf-8")
    info(f"Output from command:\n{output}")
    return output
