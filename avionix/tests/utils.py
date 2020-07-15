import re
from subprocess import check_output

from pandas import DataFrame

from avionix.kubernetes_objects.container import Container
from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.kubernetes_objects.metadata import ObjectMeta
from avionix.kubernetes_objects.pod import PodSpec, PodTemplateSpec
from avionix.kubernetes_objects.selector import LabelSelector


def get_test_deployment(number: int):
    return Deployment(
        metadata=ObjectMeta(
            name=f"test-deployment-{number}", labels={"type": "master"}
        ),
        spec=DeploymentSpec(
            replicas=1,
            template=PodTemplateSpec(
                ObjectMeta(labels={"container_type": "master"}),
                spec=PodSpec(
                    containers=[Container(name="test-container", image="test-image")]
                ),
            ),
            selector=LabelSelector(match_labels={"container_type": "master"}),
        ),
    )


def space_split(output_line: str):
    return [
        value
        for value in re.split(r"(\t|  +)", output_line)
        if not re.match(r"^\s*$", value)
    ]


def parse_binary_output_to_dict(output: bin):
    output_lines = output.decode("utf-8").split("\n")
    names = space_split(output_lines[0])
    value_rows = []
    for line in output_lines[1:]:
        values = space_split(line)
        value_rows.append(values)
    print(names)
    print(value_rows)
    return DataFrame(data=value_rows, columns=names)


def get_helm_installations():
    output = check_output(["helm", "list"])
    return parse_binary_output_to_dict(output)


def kubectl_get(resource: str):
    return parse_binary_output_to_dict(check_output(["kubectl", "get", resource]))
