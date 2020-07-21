from typing import Optional

from avionix.options import DEFAULTS
from avionix.yaml.yaml_handling import HelmYaml


class KubernetesBaseObject(HelmYaml):
    """
    Base object for other kubernetes objects to inherit from
    Required fields come from
    https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/
    """

    _version_prefix = ""

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

    def _get_api_version(self, api_version: Optional[str]):
        if api_version is None:
            return self._version_prefix + DEFAULTS["default_api_version"]
        return api_version


class Apps(KubernetesBaseObject):
    """
    Base class for apps group
    """

    _version_prefix = "apps/"


class AdmissionRegistration(KubernetesBaseObject):
    """
    Base class for admission registration group
    """

    _version_prefix = "admissionregistration.k8s.io/"


class ApiExtensions(KubernetesBaseObject):
    """
    Base class for api extensions group
    """

    _version_prefix = "apiextensions.k8s.io/"


class ApiRegistration(KubernetesBaseObject):
    """
    Base class for api registration
    """

    _version_prefix = "apiregistration.k8s.io/"


class BaseSpec(HelmYaml):
    pass
