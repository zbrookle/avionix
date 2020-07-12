from typing import List

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.chart_info import ChartInfo
import os


class ChartBuilder:
    """
    Main builder object. Accepts kubernetes objects and generates the helm chart
    structure. Can also perform the installation onto the server
    """

    def __init__(self, chart_info: ChartInfo,
                 kubernetes_objects: List[KubernetesBaseObject] = None):
        self.chart_info = chart_info
        self.kubernetes_objects = kubernetes_objects
        self.__templates_directory = f'{self.chart_info.name}/templates'
        self.__chart_yaml = f'{self.chart_info.name}/chart.yaml'

    def generate_chart(self):
        os.makedirs(self.__templates_directory, exist_ok=True)
        with open(self.__chart_yaml, 'w+') as chart_yaml_file:
            chart_yaml_file.write(str(self.chart_info))
