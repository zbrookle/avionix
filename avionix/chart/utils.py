from typing import Optional

from avionix._process_utils import custom_check_output
from avionix.testing.helpers import parse_output_to_dict


def get_helm_installations(namespace: Optional[str] = None):
    command = "helm list"
    if namespace is not None:
        command += f" -n {namespace}"
    output = custom_check_output(command)
    return parse_output_to_dict(output)
