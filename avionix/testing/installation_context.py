from logging import info
import os
from pathlib import Path
import shutil
import time
from typing import Callable, Dict, Optional, Tuple

from avionix.chart import ChartBuilder
from avionix.errors import ChartAlreadyInstalledError
from avionix.testing import kubectl_get


class ChartInstallationContext:
    """
    Class to help with installing and uninstalling charts for testing
    """

    chart_id = 0

    def __init__(
        self,
        chart_builder: ChartBuilder,
        status_resource: str = "pods",
        timeout: int = 20,
        expected_status: Optional[set] = None,
        status_field: str = "STATUS",
        uninstall_func: Optional[Callable] = None,
        extra_installation_args: Optional[Dict[str, str]] = None,
        parallel: bool = False,
    ):
        self.chart_builder = chart_builder
        if parallel:
            self.chart_builder.namespace = f"test-{self.chart_id}"
            self.chart_id += 1
        self.status_resource = status_resource
        self.timeout = timeout
        if expected_status is None:
            self.expected_status = {"Running", "Success"}
        else:
            self.expected_status = expected_status
        self.__temp_dir = Path.cwd() / "tmp"
        self.__status_field = status_field
        self.__uninstall_func = uninstall_func
        self.extra_installation_args: Dict[str, str] = (
            {} if extra_installation_args is None else {}
        )

    def get_status_resources(self) -> Dict[str, Tuple[str]]:
        resources = kubectl_get(self.status_resource)
        if self.__status_field in resources:
            return resources[self.__status_field]
        return {}

    def wait_for_uninstall(self):
        while True:
            resources = self.get_status_resources()
            if not resources:
                break
            time.sleep(1)

    def __enter__(self):
        os.makedirs(str(self.__temp_dir), exist_ok=True)
        options = {"dependency-update": None, "wait": None, "create-namespace": ""}
        options.update(self.extra_installation_args)
        try:
            self.chart_builder.install_chart(options=options)
        except ChartAlreadyInstalledError:
            info("Chart already installed, uninstalling...")
            self.chart_builder.uninstall_chart()
            self.chart_builder.install_chart(options=options)
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
