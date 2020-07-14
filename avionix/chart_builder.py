import os
from pathlib import Path
import shutil
from typing import Dict, List, Optional

from avionix.chart_info import ChartInfo
from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
import subprocess


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
    ):
        self.chart_info = chart_info
        self.kubernetes_objects = kubernetes_objects
        self.chart_folder_path = Path(self.chart_info.name)
        self.__templates_directory = self.chart_folder_path / "templates"
        self.__chart_yaml = self.chart_folder_path / "Chart.yaml"
        if output_directory:
            self.__templates_directory = Path(output_directory) / str(
                self.__templates_directory
            )
            self.__chart_yaml = Path(output_directory) / str(self.__chart_yaml)

    def __delete_chart_directory(self):
        if os.path.exists(self.chart_info.name) and os.path.isdir:
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

    def __run_helm_install(self):
        try:
            subprocess.check_call(
                f"helm install {self.chart_info.name} "
                f"./{self.chart_folder_path}".split(" ")
            )
        except subprocess.CalledProcessError as err:
            subprocess.check_call(f"helm uninstall {self.chart_info.name}".split(" "))
            raise err

    def install_chart(self):
        self.generate_chart()
        self.__run_helm_install()
