from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.service import ServiceReference
from avionix.yaml.yaml_handling import HelmYaml


class APIServiceSpec(HelmYaml):
    """
    :param ca_bundle:CABundle is a PEM encoded CA bundle which will be used to \
        validate an API server's serving certificate. If unspecified, system trust \
        roots on the apiserver are used.
    :type ca_bundle: str
    :param group:Group is the API group name this server hosts
    :type group: str
    :param group_priority_minimum:GroupPriorityMininum is the priority this group \
        should have at least. Higher priority means that the group is preferred by \
        clients over lower priority ones. Note that other versions of this group might \
        specify even higher GroupPriorityMininum values such that the whole group gets \
        a higher priority. The primary sort is based on GroupPriorityMinimum, ordered \
        highest number to lowest (20 before 10). The secondary sort is based on the \
        alphabetical comparison of the name of the object.  (v1.bar before v1.foo) \
        We'd recommend something like: *.k8s.io (except extensions) at 18000 and \
        PaaSes (OpenShift, Deis) are recommended to be in the 2000s
    :type group_priority_minimum: int
    :param insecure_skip_tlsverify:InsecureSkipTLSVerify disables TLS certificate \
        verification when communicating with this server. This is strongly \
        discouraged.  You should use the CABundle instead.
    :type insecure_skip_tlsverify: bool
    :param service:Service is a reference to the service for this API server.  It must \
        communicate on port 443 If the Service is nil, that means the handling for the \
        API groupversion is handled locally on this server. The call will simply \
        delegate to the normal handler chain to be fulfilled.
    :type service: ServiceReference
    :param version:Version is the API version this server hosts.  For example, "v1"
    :type version: str
    :param version_priority:VersionPriority controls the ordering of this API version \
        inside of its group.  Must be greater than zero. The primary sort is based on \
        VersionPriority, ordered highest to lowest (20 before 10). Since it's inside \
        of a group, the number can be small, probably in the 10s. In case of equal \
        version priorities, the version string will be used to compute the order \
        inside a group. If the version string is "kube-like", it will sort above non \
        "kube-like" version strings, which are ordered lexicographically. "Kube-like" \
        versions start with a "v", then are followed by a number (the major version), \
        then optionally the string "alpha" or "beta" and another number (the minor \
        version). These are sorted first by GA > beta > alpha (where GA is a version \
        with no suffix such as beta or alpha), and then by comparing major version, \
        then minor version. An example sorted list of versions: v10, v2, v1, v11beta2, \
        v10beta3, v3beta1, v12alpha1, v11alpha2, foo1, foo10.
    :type version_priority: int
    """

    def __init__(
        self,
        ca_bundle: str,
        group: str,
        group_priority_minimum: int,
        insecure_skip_tlsverify: bool,
        service: ServiceReference,
        version: str,
        version_priority: int,
    ):
        self.caBundle = ca_bundle
        self.group = group
        self.groupPriorityMinimum = group_priority_minimum
        self.insecureSkipTLSVerify = insecure_skip_tlsverify
        self.service = service
        self.version = version
        self.versionPriority = version_priority


class APIServiceCondition(HelmYaml):
    """
    :param last_transition_time:Last time the condition transitioned from one status \
        to another.
    :type last_transition_time: time
    :param message:Human-readable message indicating details about last transition.
    :type message: str
    :param reason:Unique, one-word, CamelCase reason for the condition's last \
        transition.
    :type reason: str
    :param type:Type is the type of the condition.
    :type type: str
    """

    def __init__(
        self, last_transition_time: time, message: str, reason: str, type: str
    ):
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class APIService(KubernetesBaseObject):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:Spec contains information for locating and communicating with a server
    :type spec: APIServiceSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: APIServiceSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class GroupVersionForDiscovery(HelmYaml):
    """
    :param group_version:groupVersion specifies the API group and version in the form \
        "group/version"
    :type group_version: str
    :param version:version specifies the version in the form of "version". This is to \
        save the clients the trouble of splitting the GroupVersion.
    :type version: str
    """

    def __init__(self, group_version: str, version: str):
        self.groupVersion = group_version
        self.version = version


class ServerAddressByClientCIDR(HelmYaml):
    """
    :param client_cidr:The CIDR with which clients can match their IP to figure out \
        the server address that they should use.
    :type client_cidr: str
    :param server_address:Address of this server, suitable for a client that matches \
        the above CIDR. This can be a hostname, hostname:port, IP or IP:port.
    :type server_address: str
    """

    def __init__(self, client_cidr: str, server_address: str):
        self.clientCIDR = client_cidr
        self.serverAddress = server_address


class APIGroup(KubernetesBaseObject):
    """
    :param preferred_version:preferredVersion is the version preferred by the API \
        server, which probably is the storage version.
    :type preferred_version: GroupVersionForDiscovery
    :param server_address_by_client_cidrs:a map of client CIDR to server address that \
        is serving this group. This is to help clients reach servers in the most \
        network-efficient way possible. Clients can use the appropriate server address \
        as per the CIDR that they match. In case of multiple matches, clients should \
        use the longest matching CIDR. The server returns only those CIDRs that it \
        thinks that the client can match. For example: the master will return an \
        internal IP CIDR only, if the client reaches the server using an internal IP. \
        Server looks at X-Forwarded-For header or X-Real-Ip header or \
        request.RemoteAddr (in that order) to get the client IP.
    :type server_address_by_client_cidrs: List[ServerAddressByClientCIDR]
    :param versions:versions are the versions supported in this group.
    :type versions: List[GroupVersionForDiscovery]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    :param name:name is the name of the group.
    :type name: Optional[str]
    """

    def __init__(
        self,
        preferred_version: GroupVersionForDiscovery,
        server_address_by_client_cidrs: List[ServerAddressByClientCIDR],
        versions: List[GroupVersionForDiscovery],
        api_version: Optional[str] = None,
        name: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.preferredVersion = preferred_version
        self.serverAddressByClientCIDRs = server_address_by_client_cidrs
        self.versions = versions
        self.name = name


class APIResource(KubernetesBaseObject):
    """
    :param categories:categories is a list of the grouped resources this resource \
        belongs to (e.g. 'all')
    :type categories: List[str]
    :param group:group is the preferred group of the resource.  Empty implies the \
        group of the containing resource list. For subresources, this may have a \
        different value, for example: Scale".
    :type group: str
    :param namespaced:namespaced indicates if a resource is namespaced or not.
    :type namespaced: bool
    :param short_names:shortNames is a list of suggested short names of the resource.
    :type short_names: List[str]
    :param singular_name:singularName is the singular name of the resource.  This \
        allows clients to handle plural and singular opaquely. The singularName is \
        more correct for reporting status on a single item and both singular and \
        plural are allowed from the kubectl CLI interface.
    :type singular_name: str
    :param storage_version_hash:The hash value of the storage version, the version \
        this resource is converted to when written to the data store. Value must be \
        treated as opaque by clients. Only equality comparison on the value is valid. \
        This is an alpha feature and may change or be removed in the future. The field \
        is populated by the apiserver only if the StorageVersionHash feature gate is \
        enabled. This field will remain optional even if it graduates.
    :type storage_version_hash: str
    :param verbs:verbs is a list of supported kube verbs (this includes get, list, \
        watch, create, update, patch, delete, deletecollection, and proxy)
    :type verbs: List[str]
    :param version:version is the preferred version of the resource.  Empty implies \
        the version of the containing resource list For subresources, this may have a \
        different value, for example: v1 (while inside a v1beta1 version of the core \
        resource's group)".
    :type version: str
    :param name:name is the plural name of the resource.
    :type name: Optional[str]
    """

    def __init__(
        self,
        categories: List[str],
        group: str,
        namespaced: bool,
        short_names: List[str],
        singular_name: str,
        storage_version_hash: str,
        verbs: List[str],
        version: str,
        name: Optional[str] = None,
    ):
        self.categories = categories
        self.group = group
        self.namespaced = namespaced
        self.shortNames = short_names
        self.singularName = singular_name
        self.storageVersionHash = storage_version_hash
        self.verbs = verbs
        self.version = version
        self.name = name


class APIServiceList(KubernetesBaseObject):
    """
    :param items:None
    :type items: List[APIService]
    :param metadata:None
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[APIService],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class APIVersions(KubernetesBaseObject):
    """
    :param server_address_by_client_cidrs:a map of client CIDR to server address that \
        is serving this group. This is to help clients reach servers in the most \
        network-efficient way possible. Clients can use the appropriate server address \
        as per the CIDR that they match. In case of multiple matches, clients should \
        use the longest matching CIDR. The server returns only those CIDRs that it \
        thinks that the client can match. For example: the master will return an \
        internal IP CIDR only, if the client reaches the server using an internal IP. \
        Server looks at X-Forwarded-For header or X-Real-Ip header or \
        request.RemoteAddr (in that order) to get the client IP.
    :type server_address_by_client_cidrs: List[ServerAddressByClientCIDR]
    :param versions:versions are the api versions that are available.
    :type versions: List[str]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        server_address_by_client_cidrs: List[ServerAddressByClientCIDR],
        versions: List[str],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.serverAddressByClientCIDRs = server_address_by_client_cidrs
        self.versions = versions
