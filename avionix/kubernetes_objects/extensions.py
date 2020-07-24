from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.core import TypedLocalObjectReference
from avionix.kubernetes_objects.meta import ListMeta
from avionix.kubernetes_objects.networking import Ingress
from avionix.yaml.yaml_handling import HelmYaml


class IngressBackend(HelmYaml):
    """
    :param resource:Resource is an ObjectRef to another Kubernetes resource in the \
        namespace of the Ingress object. If resource is specified, serviceName and \
        servicePort must not be specified.
    :type resource: TypedLocalObjectReference
    :param service_name:Specifies the name of the referenced service.
    :type service_name: str
    :param service_port:Specifies the port of the referenced service.
    :type service_port: str
    """

    def __init__(
        self, resource: TypedLocalObjectReference, service_name: str, service_port: str
    ):
        self.resource = resource
        self.serviceName = service_name
        self.servicePort = service_port


class IngressTLS(HelmYaml):
    """
    :param secret_name:SecretName is the name of the secret used to terminate SSL \
        traffic on 443. Field is left optional to allow SSL routing based on SNI \
        hostname alone. If the SNI host in a listener conflicts with the "Host" header \
        field used by an IngressRule, the SNI host is used for termination and value \
        of the Host header is used for routing.
    :type secret_name: str
    :param hosts:Hosts are a list of hosts included in the TLS certificate. The values \
        in this list must match the name/s used in the tlsSecret. Defaults to the \
        wildcard host setting for the loadbalancer controller fulfilling this Ingress, \
        if left unspecified.
    :type hosts: Optional[List[str]]
    """

    def __init__(self, secret_name: str, hosts: Optional[List[str]] = None):
        self.secretName = secret_name
        self.hosts = hosts


class IngressList(KubernetesBaseObject):
    """
    :param items:Items is the list of Ingress.
    :type items: List[Ingress]
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[Ingress],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
