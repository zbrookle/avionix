from subprocess import check_output

from avionix.testing.helpers import parse_binary_output_to_dataframe


def get_helm_installations():
    output = check_output(["helm", "list"])
    return parse_binary_output_to_dataframe(output)
