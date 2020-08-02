from subprocess import check_output, STDOUT


def custom_check_output(command: str):
    return check_output(command.split(" "), stderr=STDOUT).decode("utf-8")
