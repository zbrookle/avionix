from typing import Optional

from avionix._process_utils import custom_check_output
from avionix.kube.base_objects import HelmYaml


class ChartDependency(HelmYaml):
    """
    An object that is equivalent to listing a chart dependency in chart info in helm

    You can also set the values.yaml through this configuration to set any values
    that need to be configured within dependencies

    :param name: Name of chart
    :param version: The version of the chart
    :param repository: The url of the repository that this chart originates from
    :param values: A dictionary representing the yaml to be output in the values.yaml \
        file for this dependency
    """

    def __init__(
        self,
        name: str,
        version: str,
        repository: str,
        local_repo_name: str,
        values: Optional[dict] = None,
    ):
        self.name = name
        self.version = version
        self.repository = repository
        self.__values = values
        self.__local_repo_name = local_repo_name

    def get_values_yaml(self):
        return {self.name: self.__values}

    def add_repo(self):
        custom_check_output(f"helm repo add {self.__local_repo_name} {self.repository}")

    @property
    def local_repo_name(self):
        return self.__local_repo_name
