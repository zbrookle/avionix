from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.meta import ListMeta, ObjectMeta
from avionix.kubernetes_objects.reference import ObjectReference
from avionix.yaml.yaml_handling import HelmYaml


class EndpointPort(HelmYaml):
    """
    :param app_protocol:The application protocol for this port. This field follows \
        standard Kubernetes label syntax. Un-prefixed names are reserved for IANA \
        standard service names (as per RFC-6335 and \
        http://www.iana.org/assignments/service-names). Non-standard protocols should \
        use prefixed names such as mycompany.com/my-custom-protocol.
    :type app_protocol: str
    :param name:The name of this port. All ports in an EndpointSlice must have a \
        unique name. If the EndpointSlice is dervied from a Kubernetes service, this \
        corresponds to the Service.ports[].name. Name must either be an empty string \
        or pass DNS_LABEL validation: * must be no more than 63 characters long. * \
        must consist of lower case alphanumeric characters or '-'. * must start and \
        end with an alphanumeric character. Default is empty string.
    :type name: Optional[str]
    :param port:The port number of the endpoint. If this is not specified, ports are \
        not restricted and must be interpreted in the context of the specific \
        consumer.
    :type port: Optional[int]
    :param protocol:The IP protocol for this port. Must be UDP, TCP, or SCTP. Default \
        is TCP.
    :type protocol: Optional[str]
    """

    def __init__(
        self,
        app_protocol: str,
        name: Optional[str] = None,
        port: Optional[int] = None,
        protocol: Optional[str] = None,
    ):
        self.appProtocol = app_protocol
        self.name = name
        self.port = port
        self.protocol = protocol


class EndpointConditions(HelmYaml):
    """
    :param ready:ready indicates that this endpoint is prepared to receive traffic, \
        according to whatever system is managing the endpoint. A nil value indicates \
        an unknown state. In most cases consumers should interpret this unknown state \
        as ready.
    :type ready: bool
    """

    def __init__(self, ready: bool):
        self.ready = ready


class Endpoint(HelmYaml):
    """
    :param addresses:addresses of this endpoint. The contents of this field are \
        interpreted according to the corresponding EndpointSlice addressType field. \
        Consumers must handle different types of addresses in the context of their own \
        capabilities. This must contain at least one address but no more than 100.
    :type addresses: List[str]
    :param conditions:conditions contains information about the current status of the \
        endpoint.
    :type conditions: EndpointConditions
    :param hostname:hostname of this endpoint. This field may be used by consumers of \
        endpoints to distinguish endpoints from each other (e.g. in DNS names). \
        Multiple endpoints which use the same hostname should be considered fungible \
        (e.g. multiple A values in DNS). Must pass DNS Label (RFC 1123) validation.
    :type hostname: str
    :param target_ref:targetRef is a reference to a Kubernetes object that represents \
        this endpoint.
    :type target_ref: ObjectReference
    :param topology:topology contains arbitrary topology information associated with \
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
    :type topology: dict
    """

    def __init__(
        self,
        addresses: List[str],
        conditions: EndpointConditions,
        hostname: str,
        target_ref: ObjectReference,
        topology: dict,
    ):
        self.addresses = addresses
        self.conditions = conditions
        self.hostname = hostname
        self.targetRef = target_ref
        self.topology = topology


class EndpointSlice(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata.
    :type metadata: ObjectMeta
    :param address_type:addressType specifies the type of address carried by this \
        EndpointSlice. All addresses in this slice must be the same type. This field \
        is immutable after creation. The following address types are currently \
        supported: * IPv4: Represents an IPv4 Address. * IPv6: Represents an IPv6 \
        Address. * FQDN: Represents a Fully Qualified Domain Name.
    :type address_type: str
    :param endpoints:endpoints is a list of unique endpoints in this slice. Each slice \
        may include a maximum of 1000 endpoints.
    :type endpoints: List[Endpoint]
    :param ports:ports specifies the list of network ports exposed by each endpoint in \
        this slice. Each port must have a unique name. When ports is empty, it \
        indicates that there are no defined ports. When a port is defined with a nil \
        port value, it indicates "all ports". Each slice may include a maximum of 100 \
        ports.
    :type ports: List[EndpointPort]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        address_type: str,
        endpoints: List[Endpoint],
        ports: List[EndpointPort],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.addressType = address_type
        self.endpoints = endpoints
        self.ports = ports


class EndpointSliceList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata.
    :type metadata: ListMeta
    :param items:List of endpoint slices
    :type items: List[EndpointSlice]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[EndpointSlice],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items
