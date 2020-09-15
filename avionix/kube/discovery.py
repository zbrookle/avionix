"""
Various Endpoint related classes
"""

from typing import List, Optional

from avionix.kube.base_objects import Discovery
from avionix.kube.core import EndpointPort
from avionix.kube.meta import ObjectMeta
from avionix.kube.reference import ObjectReference
from avionix.yaml.yaml_handling import HelmYaml


class EndpointConditions(HelmYaml):
    """
    :param ready: ready indicates that this endpoint is prepared to receive traffic, \
        according to whatever system is managing the endpoint. A nil value indicates \
        an unknown state. In most cases consumers should interpret this unknown state \
        as ready.
    """

    def __init__(self, ready: bool):
        self.ready = ready


class Endpoint(HelmYaml):
    """
    :param addresses: addresses of this endpoint. The contents of this field are \
        interpreted according to the corresponding EndpointSlice addressType field. \
        Consumers must handle different types of addresses in the context of their own \
        capabilities. This must contain at least one address but no more than 100.
    :param conditions: conditions contains information about the current status of the \
        endpoint.
    :param hostname: hostname of this endpoint. This field may be used by consumers of \
        endpoints to distinguish endpoints from each other (e.g. in DNS names). \
        Multiple endpoints which use the same hostname should be considered fungible \
        (e.g. multiple A values in DNS). Must pass DNS Label (RFC 1123) validation.
    :param target_ref: targetRef is a reference to a Kubernetes object that represents \
        this endpoint.
    :param topology: topology contains arbitrary topology information associated with \
        the endpoint. These key/value pairs must conform with the label format. \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels \
        Topology may include a maximum of 16 key/value pairs. This includes, but is \
        not limited to the following well known keys: * kubernetes.io/hostname: the \
        value indicates the hostname of the node   where the endpoint is located. This \
        should match the corresponding   node label. * topology.kubernetes.io/zone: \
        the value indicates the zone where the   endpoint is located. This should \
        match the corresponding node label. * topology.kubernetes.io/region: the value \
        indicates the region where the   endpoint is located. This should match the \
        corresponding node label.
    """

    def __init__(
        self,
        addresses: List[str],
        conditions: Optional[EndpointConditions] = None,
        hostname: Optional[str] = None,
        target_ref: Optional[ObjectReference] = None,
        topology: Optional[dict] = None,
    ):
        self.addresses = addresses
        self.conditions = conditions
        self.hostname = hostname
        self.targetRef = target_ref
        self.topology = topology


class EndpointSlice(Discovery):
    """
    :param metadata: Standard object's metadata.
    :param address_type: addressType specifies the type of address carried by this \
        EndpointSlice. All addresses in this slice must be the same type. This field \
        is immutable after creation. The following address types are currently \
        supported: * IPv4: Represents an IPv4 Address. * IPv6: Represents an IPv6 \
        Address. * FQDN: Represents a Fully Qualified Domain Name.
    :param endpoints: endpoints is a list of unique endpoints in this slice. Each slice \
        may include a maximum of 1000 endpoints.
    :param ports: ports specifies the list of network ports exposed by each endpoint in \
        this slice. Each port must have a unique name. When ports is empty, it \
        indicates that there are no defined ports. When a port is defined with a nil \
        port value, it indicates "all ports". Each slice may include a maximum of 100 \
        ports.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    _non_standard_version = "v1beta1"

    def __init__(
        self,
        metadata: ObjectMeta,
        address_type: str,
        endpoints: List[Endpoint],
        ports: Optional[List[EndpointPort]] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.addressType = address_type
        self.endpoints = endpoints
        self.ports = ports
