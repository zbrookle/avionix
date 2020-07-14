import os
import shutil
from typing import Dict, List

from avionix.chart_info import ChartInfo
from avionix.kubernetes_objects.base_objects import KubernetesBaseObject


class ChartBuilder:
    """
    Main builder object. Accepts kubernetes objects and generates the helm chart
    structure. Can also perform the installation onto the server
    """

    def __init__(
        self, chart_info: ChartInfo, kubernetes_objects: List[KubernetesBaseObject]
    ):
        self.chart_info = chart_info
        self.kubernetes_objects = kubernetes_objects
        self.__templates_directory = f"{self.chart_info.name}/templates"
        self.__chart_yaml = f"{self.chart_info.name}/chart.yaml"

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
            print(kubernetes_object.kind)
            if kubernetes_object.kind not in kind_count:
                kind_count[kubernetes_object.kind] = 0
            else:
                kind_count[kubernetes_object.kind] += 1
            with open(
                f"{self.__templates_directory}/{kubernetes_object.kind}-"
                f"{kind_count[kubernetes_object.kind]}.yaml",
                "w",
            ) as template:
                print(str(kubernetes_object))
                template.write(str(kubernetes_object))
