from logging import info
import re
from subprocess import check_output
import time

from pandas import DataFrame, Series

from avionix.chart import ChartBuilder
from avionix.kubernetes_objects.container import Container
from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.kubernetes_objects.metadata import ObjectMeta
from avionix.kubernetes_objects.pod import PodSpec, PodTemplateSpec
from avionix.kubernetes_objects.selector import LabelSelector
from avionix.errors import ChartAlreadyInstalledError

def get_test_container(number: int):
    return Container(name=f"test-container-{number}", image="k8s.gcr.io/echoserver:1.4")

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
                    containers=[
                        get_test_container(number)
                    ]
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


def parse_binary_output_to_dataframe(output: bin):
    output_lines = output.decode("utf-8").split("\n")
    names = space_split(output_lines[0])
    value_rows = []
    for line in output_lines[1:]:
        values = space_split(line)
        if values:
            value_rows.append(values)
    df = DataFrame(data=value_rows, columns=names)
    info("\n" + str(df))
    return df


def get_helm_installations():
    output = check_output(["helm", "list"])
    return parse_binary_output_to_dataframe(output)


def kubectl_get(resource: str):
    return parse_binary_output_to_dataframe(check_output(["kubectl", "get", resource]))


class ChartInstallationContext:
    """
    Class to help with installing and uninstalling charts for testing
    """

    def __init__(
        self,
        chart_builder: ChartBuilder,
        status_resource: str = "pods",
        timeout: int = 20,
    ):
        self.chart_builder = chart_builder
        self.status_resource = status_resource
        self.timeout = timeout

    def get_status_resources(self) -> Series:
        resources = kubectl_get(self.status_resource)
        if "STATUS" in resources:
            return resources["STATUS"]
        return Series([])

    def wait_for_ready(self):
        tries = 0
        expected_status = {"Running", "Success"}
        while True:
            resources = self.get_status_resources()
            expected_success_count = len(resources)
            successes = sum(
                [1 if status in expected_status else 0 for status in resources]
            )
            if successes == expected_success_count:
                break
            time.sleep(5)
            tries += 1
            if tries == self.timeout:
                raise Exception("Waited too too long for installation to succeed")

    def wait_for_uninstall(self):
        while True:
            resources = self.get_status_resources()
            if resources.empty:
                break
            time.sleep(1)

    def __enter__(self):
        try:
            self.chart_builder.install_chart()
        except ChartAlreadyInstalledError:
            info("Chart already installed, uninstalling...")
            self.chart_builder.uninstall_chart()
            self.chart_builder.install_chart()
        self.wait_for_ready()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.chart_builder.uninstall_chart()
        self.wait_for_uninstall()
