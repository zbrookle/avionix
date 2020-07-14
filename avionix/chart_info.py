from typing import List, Optional

from avionix.chart_dependency import ChartDependency
from avionix.kubernetes_objects.base_objects import HelmYaml


class ChartInfo(HelmYaml):
    def __init__(
        self,
        api_version: str,
        name: str,
        version: str,
        kube_version: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[str] = None,
        key_words: Optional[List[str]] = None,
        home: Optional[str] = None,
        sources: Optional[List[str]] = None,
        dependencies: Optional[List[ChartDependency]] = None,
    ):

        self.apiVersion = api_version
        self.name = name
        self.version = version
        self.kubeVersion = kube_version
        self.description = description
        self.type = type
        self.keywords = key_words
        self.home = home
        self.sources = sources
        self.dependencies = dependencies
