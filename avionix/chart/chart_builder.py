from logging import error, info
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import Dict, List, Optional

import yaml

from avionix._process_utils import custom_check_output
from avionix.chart.chart_info import ChartInfo
from avionix.chart.utils import get_helm_installations
from avionix.chart.values_yaml import Values
from avionix.errors import (
    ChartNotInstalledError,
    ErrorFactory,
    post_uninstall_handle_error,
)
from avionix.kube.base_objects import KubernetesBaseObject


class ChartBuilder:
    """
    Main builder object. Accepts kubernetes objects and generates the helm chart
    structure. Can also perform the installation onto the server

    :param chart_info: Contains all chart metadata and dependency info
    :param kubernetes_objects: A list of kubernetes objects
    :param output_directory: A path to the directory in which to place the generated \
        chart
    :param keep_chart: Whether or not to keep the chart after installation
    :param namespace: The namespace in which all chart components should be installed \
        This allows the convenience of not passing the namespace option to both \
        install and uninstall
    """

    def __init__(
        self,
        chart_info: ChartInfo,
        kubernetes_objects: List[KubernetesBaseObject],
        output_directory: Optional[str] = None,
        keep_chart: bool = False,
        namespace: Optional[str] = None,
        values: Optional[Values] = None,
    ):
        self.chart_info = chart_info
        self.kubernetes_objects = kubernetes_objects
        self.chart_folder_path = Path(self.chart_info.name)
        self.__templates_directory = self.chart_folder_path / "templates"
        self.__chart_yaml = self.chart_folder_path / "Chart.yaml"
        self.__keep_chart = keep_chart
        self.__values = values
        self.namespace = namespace
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
        """
        Generates the chart but does not install it on kubernetes

        :returns The template directory
        """
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
        return self.__templates_directory

    def _helm_list_repos(self) -> List[str]:
        try:
            return custom_check_output("helm repo list").split("\n")[1:]
        except subprocess.CalledProcessError as err:
            error_message = err.output.decode("utf-8").strip()
            if error_message == "Error: no repositories to show":
                return []
            error(error_message)
            raise err

    def get_helm_repos(self):
        repo_lines = self._helm_list_repos()
        repo_to_url_dict = {}
        for repo_line in repo_lines:
            repo_line_no_extra_space = repo_line.strip()
            match = re.match(
                "(?P<repo_name>.+?)\s+(?P<url>.+)", repo_line_no_extra_space
            )
            if not repo_line_no_extra_space:
                continue
            if not match:
                raise Exception(
                    f"Could not match repo name pattern from output for "
                    f"line {repo_line_no_extra_space}"
                )
            repo_to_url_dict[match.group("repo_name")] = match.group("url")
        return repo_to_url_dict

    def add_dependency_repos(self):
        """
        Adds repos for all dependencies listed
        """
        info("Adding dependencies...")
        installed_repos = self.get_helm_repos()
        for dependency in self.chart_info.dependencies:
            if installed_repos.get(dependency.local_repo_name) == dependency.repository:
                continue
            dependency.add_repo()

    def __get_values_yaml(self):
        values = {}
        for dependency in self.chart_info.dependencies:
            values.update(dependency.get_values_yaml())
        if self.__values:
            values.update(self.__values.values)
        return yaml.dump(values)

    @staticmethod
    def __parse_options(options: Optional[Dict[str, Optional[str]]] = None):
        option_string = ""
        if options is None:
            return option_string
        for option in options:
            option_string += f" --{option}"

            # Add value after flag if one is given
            value = options[option]
            if value:
                option_string += f" {value}"
        return option_string

    def __get_helm_install_command(
        self, options: Optional[Dict[str, Optional[str]]] = None
    ):
        command = (
            f"helm install {self.chart_info.name} {self.chart_folder_path.resolve()}"
        )
        return self.__handle_namespace(command) + self.__parse_options(options)

    def run_helm_install(self, options: Optional[Dict[str, Optional[str]]] = None):
        """
        Runs helm install on the chart

        :param options: A dictionary of command line arguments to pass to helm

        :Example:

        To run an install with updated dependencies and with verbose logging:

        >>> self.run_helm_install({"dependency_update": None, "v": "info"})
        """
        custom_check_output(self.__get_helm_install_command(options))

    def __handle_installation(self, options: Optional[Dict[str, Optional[str]]] = None):
        try:
            info(f"Installing helm chart {self.chart_info.name}...")
            self.run_helm_install(options)
        except subprocess.CalledProcessError as err:
            decoded = err.output.decode("utf-8")
            error = ErrorFactory(decoded).get_error()
            if error is not None:
                raise error
            if self.is_installed:
                self.uninstall_chart()
            raise post_uninstall_handle_error(decoded)

    def install_chart(self, options: Optional[Dict[str, Optional[str]]] = None):
        """
        Generates and installs the helm chart onto kubernetes and handles all failures.
        It will also add the repos of all listed dependencies.

        Note that the generated chart will be deleted if *keep_chart* is not set to
        true on ChartBuilder

        WARNING: If the helm chart installation fails, the chart will be uninstalled,
        so if working with an existing chart, please use upgrade_chart instead

        :param options: A dictionary of command line arguments to pass to helm

        For example, to run an install with updated dependencies and with verbose
        logging:
        >>> self.helm_install({"dependency_update": None, "v": "info"})
        """
        self.generate_chart()
        self.add_dependency_repos()
        self.__handle_installation(options)
        if not self.__keep_chart:
            self.__delete_chart_directory()

    def __get_helm_uninstall_command(
        self, options: Optional[Dict[str, Optional[str]]] = None
    ):
        command = f"helm uninstall {self.chart_info.name}"
        return self.__handle_namespace(command) + self.__parse_options(options)

    def run_helm_uninstall(self, options: Optional[Dict[str, Optional[str]]] = None):
        """
        Runs helm uninstall

        :param options: A dictionary of command line arguments to pass to helm

        :Example:

        >>> self.run_helm_uninstall(
        >>>    {"dry-run": None,
        >>>    "description": "My uninstall description"
        >>>    }
        >>> )
        """
        info(f"Uninstalling chart {self.chart_info.name}")
        custom_check_output(self.__get_helm_uninstall_command(options))

    def __check_if_installed(self):
        info(f"Checking if helm chart {self.chart_info.name} is installed")
        if not self.is_installed:
            raise ChartNotInstalledError(
                f'Error: chart "{self.chart_info.name}" is not installed'
            )

    def __handle_uninstallation(
        self, options: Optional[Dict[str, Optional[str]]] = None
    ):
        self.__check_if_installed()
        self.run_helm_uninstall(options)

    def uninstall_chart(self, options: Optional[Dict[str, Optional[str]]] = None):
        """
        Uninstalls the chart if present, if not present, raises an error

        :param options: A dictionary of command line arguments to pass to helm

        :Example:

        >>> self.uninstall_chart(
        >>>    {"dry-run": None,
        >>>    "description": "My uninstall description"
        >>>    }
        >>> )
        """
        self.__handle_uninstallation(options)

    def __handle_namespace(self, command: str):
        if self.namespace is not None:
            return command + f" -n {self.namespace}"
        return command

    def __get_helm_upgrade_command(
        self, options: Optional[Dict[str, Optional[str]]] = None
    ):
        command = f"helm upgrade {self.chart_info.name} {self.chart_folder_path}"
        return self.__handle_namespace(command) + self.__parse_options(options)

    def __handle_upgrade(self, options: Optional[Dict[str, Optional[str]]] = None):
        try:
            self.run_helm_upgrade(options)
        except subprocess.CalledProcessError as err:
            decoded = err.output.decode("utf-8")
            error = ErrorFactory(decoded).get_error()
            if error is not None:
                raise error
            raise post_uninstall_handle_error(decoded)

    def run_helm_upgrade(self, options: Optional[Dict[str, Optional[str]]] = None):
        """
        Runs 'helm upgrade' on the chart

        :param options: A dictionary of command line arguments to pass to helm

        :Example:

        >>> self.run_helm_upgrade(options={"atomic": None, "version": "2.0"})
        """
        info(f"Upgrading helm chart {self.chart_info.name}")
        custom_check_output(self.__get_helm_upgrade_command(options))

    def upgrade_chart(self, options: Optional[Dict[str, Optional[str]]] = None):
        """
        Generates and upgrades the helm chart

        :param options: A dictionary of command line arguments to pass to helm

        :Example:

        >>> self.upgrade_chart(options={"atomic": None, "version": "2.0"})
        """
        self.__check_if_installed()
        self.generate_chart()
        self.add_dependency_repos()
        update_depenedencies = "dependency-update"
        if options is not None and update_depenedencies in options:
            custom_check_output(
                f"helm dependency update {self.chart_folder_path.resolve()}"
            )
            del options[update_depenedencies]
        self.__handle_upgrade(options)

    @property
    def is_installed(self):
        """
        :return: True if chart with the given name is already installed in the chart \
            builders namespace, else False
        """
        installations = get_helm_installations(self.namespace)
        if not installations:
            return False
        return self.chart_info.name in installations["NAME"]
