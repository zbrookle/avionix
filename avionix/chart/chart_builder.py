from logging import info
import os
from pathlib import Path
import shutil
import subprocess
from typing import Dict, List, Optional

from avionix._process_utils import custom_check_output
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
        namespace: Optional[str] = None,
        create_namespace: bool = False,
    ):
        self.chart_info = chart_info
        self.kubernetes_objects = kubernetes_objects
        self.chart_folder_path = Path(self.chart_info.name)
        self.__templates_directory = self.chart_folder_path / "templates"
        self.__chart_yaml = self.chart_folder_path / "Chart.yaml"
        self.__keep_chart = keep_chart
        self.__namespace = namespace
        self.__create_namespace = create_namespace
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
        with open(
            self.__templates_directory.parent / "values.yaml", "w"
        ) as values_file:
            values_file.write(self.__get_values_yaml())

    def update_dependencies(self):
        for dependency in self.chart_info.dependencies:
            dependency.add_repo()
        custom_check_output(
            f"helm dependencies update {self.chart_folder_path.resolve()}"
        )

    def __get_values_yaml(self):
        values_text = ""
        for dependency in self.chart_info.dependencies:
            values_text += dependency.get_values_yaml() + "\n"
        return values_text

    def __handle_namespace(self, command: str):
        if self.__namespace is not None:
            return command + f" -n {self.__namespace}"
        return command

    def __get_helm_install_command(self):
        command = (
            f"helm install {self.chart_info.name} {self.chart_folder_path.resolve()}"
        )
        if self.__create_namespace:
            command += " --create-namespace"
        return self.__handle_namespace(command)

    def run_helm_install(self):
        custom_check_output(self.__get_helm_install_command())

    def __handle_installation(self):
        try:
            info(f"Installing helm chart {self.chart_info.name}...")
            self.run_helm_install()
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
        self.update_dependencies()
        self.__handle_installation()
        if not self.__keep_chart:
            self.__delete_chart_directory()

    def __get_helm_uninstall_command(self):
        command = f"helm uninstall {self.chart_info.name}"
        return self.__handle_namespace(command)

    def run_helm_uninstall(self):
        info(f"Uninstalling chart {self.chart_info.name}")
        custom_check_output(self.__get_helm_uninstall_command())

    def __check_if_installed(self):
        info(f"Checking if helm chart {self.chart_info.name} is installed")
        if not self.is_installed:
            raise ChartNotInstalledError(
                f'Error: chart "{self.chart_info.name}" is not installed'
            )

    def __handle_uninstallation(self):
        self.__check_if_installed()
        self.run_helm_uninstall()

    def uninstall_chart(self):
        self.__handle_uninstallation()

    def __get_helm_upgrade_command(self):
        command = f"helm upgrade {self.chart_info.name} {self.chart_folder_path}"
        return self.__handle_namespace(command)

    def __handle_upgrade(self):
        try:
            self.__check_if_installed()
            self.update_dependencies()
            self.generate_chart()
            self.run_helm_upgrade()
        except subprocess.CalledProcessError as err:
            decoded = err.output.decode("utf-8")
            error = ErrorFactory(decoded).get_error()
            if error is not None:
                raise error
            raise post_uninstall_handle_error(decoded)

    def run_helm_upgrade(self):
        info(f"Upgrading helm chart {self.chart_info.name}")
        custom_check_output(self.__get_helm_upgrade_command())

    def upgrade_chart(self):
        self.generate_chart()
        self.__handle_upgrade()

    @property
    def is_installed(self):
        installations = get_helm_installations(self.__namespace)
        filtered = installations[installations["NAME"] == self.chart_info.name]
        return not filtered.empty
