from logging import info
import os
from pathlib import Path
import re
import shutil
from subprocess import check_output
import time
from typing import Any, List, Optional, Tuple

from pandas import DataFrame, Series

from avionix.chart import ChartBuilder
from avionix.errors import ChartAlreadyInstalledError
from avionix.kubernetes_objects.apps import Deployment, DeploymentSpec
from avionix.kubernetes_objects.core import (
    Container,
    EnvVar,
    PodSpec,
    PodTemplateSpec,
    ContainerPort,
)
from avionix.kubernetes_objects.meta import LabelSelector, ObjectMeta


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


def space_split(output_line: str):
    return [
        value
        for value in re.split(r"(\t|  +)", output_line)
        if not re.match(r"^\s*$", value)
    ]


def get_name_locations(names: List[str], name_string: str):
    locs: List[Any] = []
    last_pos = 0
    for name in names:
        last_pos = name_string.find(name, last_pos)
        locs.append(last_pos)
    for i, loc in enumerate(locs):
        if i + 1 < len(locs):
            locs[i] = (loc, locs[i + 1])
            continue
        locs[i] = (loc, len(name_string))
    return locs


def split_using_locations(locations: List[Tuple[int, int]], values_string: str):
    vals = []
    for i, loc in enumerate(locations):
        start = loc[0]
        end = loc[1]
        if i == len(locations) - 1:
            vals.append(values_string[start:].strip())
            continue
        vals.append(values_string[start:end].strip())
    return vals


def parse_binary_output_to_dataframe(output: bytes):
    output_lines = output.decode("utf-8").split("\n")
    names = space_split(output_lines[0])
    value_locations = get_name_locations(names, output_lines[0])
    value_rows = []
    for line in output_lines[1:]:
        if line.strip():
            values = split_using_locations(value_locations, line)
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
        expected_status: Optional[set] = None,
    ):
        self.chart_builder = chart_builder
        self.status_resource = status_resource
        self.timeout = timeout
        if expected_status is None:
            self.expected_status = {"Running", "Success"}
        else:
            self.expected_status = expected_status
        self.__temp_dir = Path.cwd() / "tmp"

    def get_status_resources(self) -> Series:
        resources = kubectl_get(self.status_resource)
        if "STATUS" in resources:
            return resources["STATUS"]
        return Series([], dtype="object")

    def wait_for_ready(self):
        tries = 0
        while True:
            resources = self.get_status_resources()
            expected_success_count = len(resources)
            successes = sum(
                [1 if status in self.expected_status else 0 for status in resources]
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
        os.makedirs(str(self.__temp_dir), exist_ok=True)
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
        shutil.rmtree(self.__temp_dir)
        if os.path.exists(str(self.__temp_dir)):
            raise Exception("Should not exist")
