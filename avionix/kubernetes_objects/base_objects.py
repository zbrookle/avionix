from typing import Optional

from avionix.options import DEFAULTS
from avionix.yaml.yaml_handling import HelmYaml


class KubernetesBaseObject(HelmYaml):
    """
    Base object for other kubernetes objects to inherit from
    Required fields come from
    https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/
    """

    def __init__(
        self,
        api_version: Optional[str] = None,
        kind: Optional[str] = None,
        metadata=None,
    ):
        if kind is None:
            self.kind = type(self).__name__
        else:
            self.kind = kind

        if api_version is None:
            self.apiVersion = DEFAULTS["default_api_version"]
        else:
            self.apiVersion = api_version

        self.metadata = metadata


class BaseSpec(HelmYaml):
    pass
