from logging import info
import os
from pathlib import Path
import shutil
import time
from typing import Optional, Callable

from pandas import Series

from avionix.chart import ChartBuilder
from avionix.errors import ChartAlreadyInstalledError
from avionix.testing import kubectl_get


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
        status_field: str = "STATUS",
        uninstall_func: Callable = None
    ):
        self.chart_builder = chart_builder
        self.status_resource = status_resource
        self.timeout = timeout
        if expected_status is None:
            self.expected_status = {"Running", "Success"}
        else:
            self.expected_status = expected_status
        self.__temp_dir = Path.cwd() / "tmp"
        self.__status_field = status_field
        self.__uninstall_func = uninstall_func

    def get_status_resources(self) -> Series:
        resources = kubectl_get(self.status_resource)
        if self.__status_field in resources:
            return resources[self.__status_field]
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
        if self.__uninstall_func is not None:
            self.__uninstall_func()
        else:
            self.chart_builder.uninstall_chart()
            self.wait_for_uninstall()
        shutil.rmtree(self.__temp_dir)
        if os.path.exists(str(self.__temp_dir)):
            raise Exception("Should not exist")
