"""
Classes making up the main interfaces for other Kubernetes classes
"""

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
    _base_object_name = "KubernetesBaseObject"
    _non_standard_version = ""

    def __init__(
        self,
        api_version: Optional[str] = None,
        kind: Optional[str] = None,
        metadata=None,
    ):
        if kind is None:
            self.kind = self.__get_kube_object_type().__name__
        else:
            self.kind = kind

        self.apiVersion = self._get_api_version(api_version)

        self.metadata = metadata

    def _get_api_version(self, api_version: Optional[str]):
        if self._non_standard_version:
            return self._version_prefix + self._non_standard_version
        if api_version is None:
            return self._version_prefix + DEFAULTS["default_api_version"]
        return api_version

    def __get_kube_object_type(self):
        # Get all inherited to find classes exact kube object
        mro = type(self).__mro__
        for i, class_ in enumerate(mro):
            if class_.__name__ == type(self)._base_object_name:
                return mro[i - 2]
        raise Exception("KubernetesObject ancestor class not found!")


class Core(KubernetesBaseObject):
    """
    Base object for other kubernetes objects to inherit from
    Required fields come from
    https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/
    """


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


class Extensions(KubernetesBaseObject):
    """
    Base class for api registration
    """

    _version_prefix = "extensions/"


class Batch(KubernetesBaseObject):
    """
    Base class for api registration
    """

    _version_prefix = "batch/"


class RbacAuthorization(KubernetesBaseObject):
    """
    Base class for rbac authorization
    """

    _version_prefix = "rbac.authorization.k8s.io/"


class Storage(KubernetesBaseObject):

    _version_prefix = "storage.k8s.io/"


class Authentication(KubernetesBaseObject):

    _version_prefix = "authentication.k8s.io/"


class Authorization(KubernetesBaseObject):

    _version_prefix = "authorization.k8s.io/"


class Autoscaling(KubernetesBaseObject):

    _version_prefix = "autoscaling/"


class Coordination(KubernetesBaseObject):

    _version_prefix = "coordination.k8s.io/"


class Networking(KubernetesBaseObject):

    _version_prefix = "networking.k8s.io/"


class Node(KubernetesBaseObject):

    _version_prefix = "node.k8s.io/"


class Scheduling(KubernetesBaseObject):

    _version_prefix = "scheduling.k8s.io/"


class Policy(KubernetesBaseObject):

    _version_prefix = "policy/"


class Certificates(KubernetesBaseObject):

    _version_prefix = "certificates.k8s.io/"


class Discovery(KubernetesBaseObject):

    _version_prefix = "discovery.k8s.io/"


class Meta(KubernetesBaseObject):

    _version_prefix = "meta.k8s.io/"
