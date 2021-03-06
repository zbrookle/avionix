from typing import List, Optional

from avionix.chart.chart_dependency import ChartDependency
from avionix.chart.chart_maintainer import ChartMaintainer
from avionix.kube.base_objects import HelmYaml


class ChartInfo(HelmYaml):
    """
    :param api_version: The chart API version (required)
    :param name: The name of the chart (required)
    :param version: A SemVer 2 version (required)
    :param kube_version: A SemVer range of compatible Kubernetes versions (optional)
    :param description: A single-sentence description of this project (optional)
    :param type: The type of the chart (optional)
    :param key_words: A list of keywords about this project (optional)
    :param home: The URL of this projects home page (optional)
    :param sources: A list of URLs to source code for this project (optional)
    :param dependencies: A list of the chart requirements (optional)
    :param maintainers: A list of maintainers
    :param icon: A URL to an SVG or PNG image to be used as an icon (optional).
    :param app_version: The version of the app that this contains (optional). This \
        needn't be SemVer.
    :param deprecated: Whether this chart is deprecated (optional, boolean)
    :param annotations: A list of annotations keyed by name (optional).
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
        dependencies: Optional[List[ChartDependency]] = None,
        maintainers: Optional[List[ChartMaintainer]] = None,
        icon: Optional[str] = None,
        app_version: Optional[str] = None,
        deprecated: Optional[bool] = None,
        annotations: Optional[dict] = None,
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
        self.dependencies = dependencies if dependencies is not None else []
        self.maintainers = maintainers
        self.icon = icon
        self.appVersion = app_version
        self.deprecated = deprecated
        self.annotations = annotations
