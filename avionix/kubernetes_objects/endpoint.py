from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.reference import ObjectReference
from avionix.yaml.yaml_handling import HelmYaml


class EndpointPort(HelmYaml):
    """
    :param app_protocol:The application protocol for this port. This field follows \
        standard Kubernetes label syntax. Un-prefixed names are reserved for IANA \
        standard service names (as per RFC-6335 and \
        http://www.iana.org/assignments/service-names). Non-standard protocols should \
        use prefixed names such as mycompany.com/my-custom-protocol. Field can be \
        enabled with ServiceAppProtocol feature gate.
    :type app_protocol: str
    :param port:The port number of the endpoint.
    :type port: int
    :param name:The name of this port.  This must match the 'name' field in the \
        corresponding ServicePort. Must be a DNS_LABEL. Optional only if one port is \
        defined.
    :type name: Optional[str]
    :param protocol:The IP protocol for this port. Must be UDP, TCP, or SCTP. Default \
        is TCP.
    :type protocol: Optional[str]
    """

    def __init__(
        self,
        app_protocol: str,
        port: int,
        name: Optional[str] = None,
        protocol: Optional[str] = None,
    ):
        self.appProtocol = app_protocol
        self.port = port
        self.name = name
        self.protocol = protocol


class EndpointAddress(HelmYaml):
    """
    :param hostname:The Hostname of this endpoint
    :type hostname: str
    :param ip:The IP of this endpoint. May not be loopback (127.0.0.0/8), link-local \
        (169.254.0.0/16), or link-local multicast ((224.0.0.0/24). IPv6 is also \
        accepted but not fully supported on all platforms. Also, certain kubernetes \
        components, like kube-proxy, are not IPv6 ready.
    :type ip: str
    :param target_ref:Reference to object providing the endpoint.
    :type target_ref: ObjectReference
    :param node_name:Optional: Node hosting this endpoint. This can be used to \
        determine endpoints local to a node.
    :type node_name: Optional[str]
    """

    def __init__(
        self,
        hostname: str,
        ip: str,
        target_ref: ObjectReference,
        node_name: Optional[str] = None,
    ):
        self.hostname = hostname
        self.ip = ip
        self.targetRef = target_ref
        self.nodeName = node_name


class EndpointSubset(HelmYaml):
    """
    :param addresses:IP addresses which offer the related ports that are marked as \
        ready. These endpoints should be considered safe for load balancers and \
        clients to utilize.
    :type addresses: List[EndpointAddress]
    :param not_ready_addresses:IP addresses which offer the related ports but are not \
        currently marked as ready because they have not yet finished starting, have \
        recently failed a readiness check, or have recently failed a liveness check.
    :type not_ready_addresses: List[EndpointAddress]
    :param ports:Port numbers available on the related IP addresses.
    :type ports: Optional[List[EndpointPort]]
    """

    def __init__(
        self,
        addresses: List[EndpointAddress],
        not_ready_addresses: List[EndpointAddress],
        ports: Optional[List[EndpointPort]] = None,
    ):
        self.addresses = addresses
        self.notReadyAddresses = not_ready_addresses
        self.ports = ports


class Endpoints(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param subsets:The set of all endpoints is the union of all subsets. Addresses are \
        placed into subsets according to the IPs they share. A single address with \
        multiple ports, some of which are ready and some of which are not (because \
        they come from different containers) will result in the address being \
        displayed in different subsets for the different ports. No address will appear \
        in both Addresses and NotReadyAddresses in the same subset. Sets of addresses \
        and ports that comprise a service.
    :type subsets: List[EndpointSubset]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        subsets: List[EndpointSubset],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.subsets = subsets


class EndpointsList(KubernetesBaseObject):
    """
    :param items:List of endpoints.
    :type items: List[Endpoints]
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[Endpoints],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
