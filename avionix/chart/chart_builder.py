from logging import info
import os
from pathlib import Path
import shutil
import subprocess
from typing import Dict, List, Optional

from avionix.chart.chart_info import ChartInfo
from avionix.chart.utils import get_helm_installations
from avionix.errors import (
    ChartNotInstalledError,
    ErrorFactory,
    post_uninstall_handle_error,
)
from avionix.kubernetes_objects.base_objects import KubernetesBaseObject


class ChartBuilder:
    """
    Main builder object. Accepts kubernetes objects and generates the helm chart
    structure. Can also perform the installation onto the server
    """

    def __init__(
        self,
        chart_info: ChartInfo,
        kubernetes_objects: List[KubernetesBaseObject],
        output_directory: Optional[str] = None,
        keep_chart: bool = False,
    ):
        self.chart_info = chart_info
        self.kubernetes_objects = kubernetes_objects
        self.chart_folder_path = Path(self.chart_info.name)
        self.__templates_directory = self.chart_folder_path / "templates"
        self.__chart_yaml = self.chart_folder_path / "Chart.yaml"
        self.__keep_chart = keep_chart
        if output_directory:
            self.__templates_directory = Path(output_directory) / str(
                self.__templates_directory
            )
            self.__chart_yaml = Path(output_directory) / str(self.__chart_yaml)
            self.chart_folder_path = Path(output_directory) / str(
                self.chart_folder_path
            )

    def __delete_chart_directory(self):
        if os.path.exists(self.chart_info.name):
            shutil.rmtree(self.chart_info.name)

    def generate_chart(self):
        self.__delete_chart_directory()
        os.makedirs(self.__templates_directory, exist_ok=True)
        with open(self.__chart_yaml, "w+") as chart_yaml_file:
            chart_yaml_file.write(str(self.chart_info))

        kind_count: Dict[str, int] = {}
        for kubernetes_object in self.kubernetes_objects:
            print(kubernetes_object)
            if kubernetes_object.kind not in kind_count:
                kind_count[kubernetes_object.kind] = 0
            else:
                kind_count[kubernetes_object.kind] += 1
            with open(
                self.__templates_directory / f"{kubernetes_object.kind}-"
                f"{kind_count[kubernetes_object.kind]}.yaml",
                "w",
            ) as template:
                template.write(str(kubernetes_object))

    def __run_helm_install(self):
        try:
            info(f"Installing helm chart {self.chart_info.name}...")
            subprocess.check_output(
                f"helm install {self.chart_info.name} "
                f"{self.chart_folder_path.resolve()}".split(" "),
                stderr=subprocess.STDOUT,
            )
        except subprocess.CalledProcessError as err:
            decoded = err.output.decode("utf-8")
            error = ErrorFactory(decoded).get_error()
            if error is not None:
                raise error
            if self.is_installed:
                self.uninstall_chart()
            raise post_uninstall_handle_error(decoded)

    def install_chart(self):
        self.generate_chart()
        self.__run_helm_install()
        if not self.__keep_chart:
            self.__delete_chart_directory()

    def uninstall_chart(self):
        info(f"Uninstalling helm chart {self.chart_info.name}")
        if not self.is_installed:
            raise ChartNotInstalledError(
                f'Error: chart "{self.chart_info.name}" is not installed'
            )
        subprocess.check_call(
            f"helm uninstall {self.chart_info.name}".split(" "),
            stderr=subprocess.STDOUT,
        )

    @property
    def is_installed(self):
        installations = get_helm_installations()
        filtered = installations[installations["NAME"] == self.chart_info.name]
        return not filtered.empty
