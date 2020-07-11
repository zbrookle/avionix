from typing import List, Optional

from avionix.kubernetes_objects.base_objects import HelmYaml


class ChartInfo(HelmYaml):
    """
    Abstraction over chart.yaml
    Main builder object. Accepts kubernetes objects and generates the helm chart
    structure. Can also perform the installation onto the server
    """

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
