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

        self.apiVersion = self._get_api_version(api_version)

        self.metadata = metadata

    @staticmethod
    def _get_api_version(api_version: str):
        if api_version is None:
            return DEFAULTS["default_api_version"]
        return api_version


class Apps(KubernetesBaseObject):
    """
    Base class for apps group
    """

    @staticmethod
    def _get_api_version(api_version: str):
        if api_version is None:
            return "apps/" + DEFAULTS["default_api_version"]
        return api_version


class AdmissionRegistration(KubernetesBaseObject):
    """
    Base class for apps group
    """

    @staticmethod
    def _get_api_version(api_version: str):
        if api_version is None:
            return "admissionregistration.k8s.io/" + DEFAULTS["default_api_version"]
        return api_version


class BaseSpec(HelmYaml):
    pass
