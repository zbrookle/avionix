from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.pod import SessionAffinityConfig
from avionix.kubernetes_objects.reference import LocalObjectReference, ObjectReference
from avionix.yaml.yaml_handling import HelmYaml


class ServicePort(HelmYaml):
    """
    :param app_protocol:The application protocol for this port. This field follows \
        standard Kubernetes label syntax. Un-prefixed names are reserved for IANA \
        standard service names (as per RFC-6335 and \
        http://www.iana.org/assignments/service-names). Non-standard protocols should \
        use prefixed names such as mycompany.com/my-custom-protocol. Field can be \
        enabled with ServiceAppProtocol feature gate.
    :type app_protocol: str
    :param port:The port that will be exposed by this service.
    :type port: str
    :param name:The name of this port within the service. This must be a DNS_LABEL. \
        All ports within a ServiceSpec must have unique names. When considering the \
        endpoints for a Service, this must match the 'name' field in the EndpointPort. \
        Optional if only one ServicePort is defined on this service.
    :type name: Optional[str]
    :param node_port:The port on each node on which this service is exposed when \
        type=NodePort or LoadBalancer. Usually assigned by the system. If specified, \
        it will be allocated to the service if unused or else creation of the service \
        will fail. Default is to auto-allocate a port if the ServiceType of this \
        Service requires one. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport  # noqa
    :type node_port: Optional[int]
    :param protocol:The IP protocol for this port. Supports "TCP", "UDP", and "SCTP". \
        Default is TCP.
    :type protocol: Optional[int]
    :param target_port:Number or name of the port to access on the pods targeted by \
        the service. Number must be in the range 1 to 65535. Name must be an \
        IANA_SVC_NAME. If this is a string, it will be looked up as a named port in \
        the target Pod's container ports. If this is not specified, the value of the \
        'port' field is used (an identity map). This field is ignored for services \
        with clusterIP=None, and should be omitted or set equal to the 'port' field. \
        More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#defining-a-service  # noqa
    :type target_port: Optional[str]
    """

    def __init__(
        self,
        app_protocol: str,
        port: str,
        name: Optional[str] = None,
        node_port: Optional[int] = None,
        protocol: Optional[int] = None,
        target_port: Optional[str] = None,
    ):
        self.appProtocol = app_protocol
        self.port = port
        self.name = name
        self.nodePort = node_port
        self.protocol = protocol
        self.targetPort = target_port


class ServiceSpec(HelmYaml):
    """
    :param cluster_ip:clusterIP is the IP address of the service and is usually \
        assigned randomly by the master. If an address is specified manually and is \
        not in use by others, it will be allocated to the service; otherwise, creation \
        of the service will fail. This field can not be changed through updates. Valid \
        values are "None", empty string (""), or a valid IP address. "None" can be \
        specified for headless services when proxying is not required. Only applies to \
        types ClusterIP, NodePort, and LoadBalancer. Ignored if type is ExternalName. \
        More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies  # noqa
    :type cluster_ip: str
    :param external_ips:externalIPs is a list of IP addresses for which nodes in the \
        cluster will also accept traffic for this service.  These IPs are not managed \
        by Kubernetes.  The user is responsible for ensuring that traffic arrives at a \
        node with this IP.  A common example is external load-balancers that are not \
        part of the Kubernetes system.
    :type external_ips: List[str]
    :param external_name:externalName is the external reference that kubedns or \
        equivalent will return as a CNAME record for this service. No proxying will be \
        involved. Must be a valid RFC-1123 hostname \
        (https://tools.ietf.org/html/rfc1123) and requires Type to be ExternalName.
    :type external_name: str
    :param external_traffic_policy:externalTrafficPolicy denotes if this Service \
        desires to route external traffic to node-local or cluster-wide endpoints. \
        "Local" preserves the client source IP and avoids a second hop for \
        LoadBalancer and Nodeport type services, but risks potentially imbalanced \
        traffic spreading. "Cluster" obscures the client source IP and may cause a \
        second hop to another node, but should have good overall load-spreading.
    :type external_traffic_policy: str
    :param ip_family:ipFamily specifies whether this Service has a preference for a \
        particular IP family (e.g. IPv4 vs. IPv6).  If a specific IP family is \
        requested, the clusterIP field will be allocated from that family, if it is \
        available in the cluster.  If no IP family is requested, the cluster's primary \
        IP family will be used. Other IP fields (loadBalancerIP, \
        loadBalancerSourceRanges, externalIPs) and controllers which allocate external \
        load-balancers should use the same IP family.  Endpoints for this Service will \
        be of this family.  This field is immutable after creation. Assigning a \
        ServiceIPFamily not available in the cluster (e.g. IPv6 in IPv4 only cluster) \
        is an error condition and will fail during clusterIP assignment.
    :type ip_family: str
    :param load_balancer_ip:Only applies to Service Type: LoadBalancer LoadBalancer \
        will get created with the IP specified in this field. This feature depends on \
        whether the underlying cloud-provider supports specifying the loadBalancerIP \
        when a load balancer is created. This field will be ignored if the \
        cloud-provider does not support the feature.
    :type load_balancer_ip: str
    :param publish_not_ready_addresses:publishNotReadyAddresses, when set to true, \
        indicates that DNS implementations must publish the notReadyAddresses of \
        subsets for the Endpoints associated with the Service. The default value is \
        false. The primary use case for setting this field is to use a StatefulSet's \
        Headless Service to propagate SRV records for its Pods without respect to \
        their readiness for purpose of peer discovery.
    :type publish_not_ready_addresses: bool
    :param session_affinity_config:sessionAffinityConfig contains the configurations \
        of session affinity.
    :type session_affinity_config: SessionAffinityConfig
    :param health_check_node_port:healthCheckNodePort specifies the healthcheck \
        nodePort for the service. If not specified, HealthCheckNodePort is created by \
        the service api backend with the allocated nodePort. Will use user-specified \
        nodePort value if specified by the client. Only effects when Type is set to \
        LoadBalancer and ExternalTrafficPolicy is set to Local.
    :type health_check_node_port: Optional[int]
    :param load_balancer_source_ranges:If specified and supported by the platform, \
        this will restrict traffic through the cloud-provider load-balancer will be \
        restricted to the specified client IPs. This field will be ignored if the \
        cloud-provider does not support the feature." More info: \
        https://kubernetes.io/docs/tasks/access-application-cluster/configure-cloud-provider-firewall/  # noqa
    :type load_balancer_source_ranges: Optional[List[str]]
    :param ports:The list of ports that are exposed by this service. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies  # noqa
    :type ports: Optional[List[ServicePort]]
    :param selector:Route service traffic to pods with label keys and values matching \
        this selector. If empty or not present, the service is assumed to have an \
        external process managing its endpoints, which Kubernetes will not modify. \
        Only applies to types ClusterIP, NodePort, and LoadBalancer. Ignored if type \
        is ExternalName. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/
    :type selector: Optional[dict]
    :param session_affinity:Supports "ClientIP" and "None". Used to maintain session \
        affinity. Enable client IP based session affinity. Must be ClientIP or None. \
        Defaults to None. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#virtual-ips-and-service-proxies  # noqa
    :type session_affinity: Optional[str]
    :param topology_keys:topologyKeys is a preference-order list of topology keys \
        which implementations of services should use to preferentially sort endpoints \
        when accessing this Service, it can not be used at the same time as \
        externalTrafficPolicy=Local. Topology keys must be valid label keys and at \
        most 16 keys may be specified. Endpoints are chosen based on the first \
        topology key with available backends. If this field is specified and all \
        entries have no backends that match the topology of the client, the service \
        has no backends for that client and connections should fail. The special value \
        "*" may be used to mean "any topology". This catch-all value, if used, only \
        makes sense as the last value in the list. If this is not specified or empty, \
        no topology constraints will be applied.
    :type topology_keys: Optional[List[str]]
    :param type:type determines how the Service is exposed. Defaults to ClusterIP. \
        Valid options are ExternalName, ClusterIP, NodePort, and LoadBalancer. \
        "ExternalName" maps to the specified externalName. "ClusterIP" allocates a \
        cluster-internal IP address for load-balancing to endpoints. Endpoints are \
        determined by the selector or if that is not specified, by manual construction \
        of an Endpoints object. If clusterIP is "None", no virtual IP is allocated and \
        the endpoints are published as a set of endpoints rather than a stable IP. \
        "NodePort" builds on ClusterIP and allocates a port on every node which routes \
        to the clusterIP. "LoadBalancer" builds on NodePort and creates an external \
        load-balancer (if supported in the current cloud) which routes to the \
        clusterIP. More info: \
        https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types  # noqa
    :type type: Optional[str]
    """

    def __init__(
        self,
        cluster_ip: str,
        external_ips: List[str],
        external_name: str,
        external_traffic_policy: str,
        ip_family: str,
        load_balancer_ip: str,
        publish_not_ready_addresses: bool,
        session_affinity_config: SessionAffinityConfig,
        health_check_node_port: Optional[int] = None,
        load_balancer_source_ranges: Optional[List[str]] = None,
        ports: Optional[List[ServicePort]] = None,
        selector: Optional[dict] = None,
        session_affinity: Optional[str] = None,
        topology_keys: Optional[List[str]] = None,
        type: Optional[str] = None,
    ):
        self.clusterIP = cluster_ip
        self.externalIPs = external_ips
        self.externalName = external_name
        self.externalTrafficPolicy = external_traffic_policy
        self.ipFamily = ip_family
        self.loadBalancerIP = load_balancer_ip
        self.publishNotReadyAddresses = publish_not_ready_addresses
        self.sessionAffinityConfig = session_affinity_config
        self.healthCheckNodePort = health_check_node_port
        self.loadBalancerSourceRanges = load_balancer_source_ranges
        self.ports = ports
        self.selector = selector
        self.sessionAffinity = session_affinity
        self.topologyKeys = topology_keys
        self.type = type


class Service(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the behavior of a service. \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: ServiceSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: ServiceSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class ServiceReference(HelmYaml):
    """
    :param name:Name is the name of the service
    :type name: Optional[str]
    :param namespace:Namespace is the namespace of the service
    :type namespace: Optional[str]
    :param port:If specified, the port on the service that hosting webhook. Default to \
        443 for backward compatibility. `port` should be a valid port number (1-65535, \
        inclusive).
    :type port: Optional[int]
    """

    def __init__(
        self,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        port: Optional[int] = None,
    ):
        self.name = name
        self.namespace = namespace
        self.port = port


class ServiceAccount(KubernetesBaseObject):
    """
    :param image_pull_secrets:ImagePullSecrets is a list of references to secrets in \
        the same namespace to use for pulling any images in pods that reference this \
        ServiceAccount. ImagePullSecrets are distinct from Secrets because Secrets can \
        be mounted in the pod, but ImagePullSecrets are only accessed by the kubelet. \
        More info: \
        https://kubernetes.io/docs/concepts/containers/images/#specifying-imagepullsecrets-on-a-pod  # noqa
    :type image_pull_secrets: List[LocalObjectReference]
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param secrets:Secrets is the list of secrets allowed to be used by pods running \
        using this ServiceAccount. More info: \
        https://kubernetes.io/docs/concepts/configuration/secret
    :type secrets: List[ObjectReference]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    :param automount_service_account_token:AutomountServiceAccountToken indicates \
        whether pods running as this service account should have an API token \
        automatically mounted. Can be overridden at the pod level.
    :type automount_service_account_token: Optional[bool]
    """

    def __init__(
        self,
        image_pull_secrets: List[LocalObjectReference],
        metadata: ObjectMeta,
        secrets: List[ObjectReference],
        api_version: Optional[str] = None,
        automount_service_account_token: Optional[bool] = None,
    ):
        super().__init__(api_version)
        self.imagePullSecrets = image_pull_secrets
        self.metadata = metadata
        self.secrets = secrets
        self.automountServiceAccountToken = automount_service_account_token


class ServiceAccountList(KubernetesBaseObject):
    """
    :param items:List of ServiceAccounts. More info: \
        https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/  # noqa
    :type items: List[ServiceAccount]
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
        items: List[ServiceAccount],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class ServiceList(KubernetesBaseObject):
    """
    :param items:List of services
    :type items: List[Service]
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
        items: List[Service],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
