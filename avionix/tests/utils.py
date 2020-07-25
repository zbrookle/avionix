from subprocess import check_output

from avionix.kubernetes_objects.apps import Deployment, DeploymentSpec
from avionix.kubernetes_objects.core import (
    Container,
    ContainerPort,
    EnvVar,
    PodSpec,
    PodTemplateSpec,
)
from avionix.kubernetes_objects.meta import LabelSelector, ObjectMeta
from avionix.testing.helpers import parse_binary_output_to_dataframe


def get_test_container(number: int):
    return Container(
        name=f"test-container-{number}",
        image="k8s.gcr.io/echoserver:1.4",
        env=[EnvVar("test", "test-value")],
        ports=[ContainerPort(8080)],
    )


def get_test_deployment(number: int):
    return Deployment(
        metadata=ObjectMeta(
            name=f"test-deployment-{number}", labels={"type": "master"}
        ),
        spec=DeploymentSpec(
            replicas=1,
            template=PodTemplateSpec(
                ObjectMeta(labels={"container_type": "master"}),
                spec=PodSpec(containers=[get_test_container(number)]),
            ),
            selector=LabelSelector(match_labels={"container_type": "master"}),
        ),
    )


def get_helm_installations():
    output = check_output(["helm", "list"])
    return parse_binary_output_to_dataframe(output)
