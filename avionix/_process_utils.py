from subprocess import check_output


def custom_check_output(command: str):
    return check_output(command.split(" ")).decode("utf-8")
