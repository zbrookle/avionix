from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.core import TypedLocalObjectReference
from avionix.kubernetes_objects.extensions import IngressBackend, IngressTLS
from avionix.kubernetes_objects.meta import LabelSelector, ListMeta, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class HTTPIngressPath(HelmYaml):
    """
    :param backend:Backend defines the referenced service endpoint to which the \
        traffic will be forwarded to.
    :type backend: IngressBackend
    :param path:Path is matched against the path of an incoming request. Currently it \
        can contain characters disallowed from the conventional "path" part of a URL \
        as defined by RFC 3986. Paths must begin with a '/'. When unspecified, all \
        paths from incoming requests are matched.
    :type path: str
    :param path_type:PathType determines the interpretation of the Path matching. \
        PathType can be one of the following values: * Exact: Matches the URL path \
        exactly. * Prefix: Matches based on a URL path prefix split by '/'. Matching \
        is   done on a path element by element basis. A path element refers is the   \
        list of labels in the path split by the '/' separator. A request is a   match \
        for path p if every p is an element-wise prefix of p of the   request path. \
        Note that if the last element of the path is a substring   of the last element \
        in request path, it is not a match (e.g. /foo/bar   matches /foo/bar/baz, but \
        does not match /foo/barbaz). * ImplementationSpecific: Interpretation of the \
        Path matching is up to   the IngressClass. Implementations can treat this as a \
        separate PathType   or treat it identically to Prefix or Exact path types. \
        Implementations are required to support all path types. Defaults to \
        ImplementationSpecific.
    :type path_type: Optional[str]
    """

    def __init__(
        self, backend: IngressBackend, path: str, path_type: Optional[str] = None
    ):
        self.backend = backend
        self.path = path
        self.pathType = path_type


class HTTPIngressRuleValue(HelmYaml):
    """
    :param paths:A collection of paths that map requests to backends.
    :type paths: List[HTTPIngressPath]
    """

    def __init__(self, paths: List[HTTPIngressPath]):
        self.paths = paths


class IngressRule(HelmYaml):
    """
    :param host:Host is the fully qualified domain name of a network host, as defined \
        by RFC 3986. Note the following deviations from the "host" part of the URI as \
        defined in RFC 3986: 1. IPs are not allowed. Currently an IngressRuleValue can \
        only apply to    the IP in the Spec of the parent Ingress. 2. The `:` \
        delimiter is not respected because ports are not allowed.       Currently the \
        port of an Ingress is implicitly :80 for http and       :443 for https. Both \
        these may change in the future. Incoming requests are matched against the host \
        before the IngressRuleValue. If the host is unspecified, the Ingress routes \
        all traffic based on the specified IngressRuleValue.  Host can be "precise" \
        which is a domain name without the terminating dot of a network host (e.g. \
        "foo.bar.com") or "wildcard", which is a domain name prefixed with a single \
        wildcard label (e.g. "*.foo.com"). The wildcard character '\\*' must appear by \
        itself as the first DNS label and matches only a single label. You cannot have \
        a wildcard label by itself (e.g. Host == "*"). Requests will be matched \
        against the Host field in the following way: 1. If Host is precise, the \
        request matches this rule if the http host header is equal to Host. 2. If Host \
        is a wildcard, then the request matches this rule if the http host header is \
        to equal to the suffix (removing the first label) of the wildcard rule.
    :type host: str
    :param http:None
    :type http: HTTPIngressRuleValue
    """

    def __init__(self, host: str, http: HTTPIngressRuleValue):
        self.host = host
        self.http = http


class IngressSpec(HelmYaml):
    """
    :param ingress_class_name:IngressClassName is the name of the IngressClass cluster \
        resource. The associated IngressClass defines which controller will implement \
        the resource. This replaces the deprecated `kubernetes.io/ingress.class` \
        annotation. For backwards compatibility, when that annotation is set, it must \
        be given precedence over this field. The controller may emit a warning if the \
        field and annotation have different values. Implementations of this API should \
        ignore Ingresses without a class specified. An IngressClass resource may be \
        marked as default, which can be used to set a default value for this field. \
        For more information, refer to the IngressClass documentation.
    :type ingress_class_name: str
    :param rules:A list of host rules used to configure the Ingress. If unspecified, \
        or no rule matches, all traffic is sent to the default backend.
    :type rules: List[IngressRule]
    :param tls:TLS configuration. Currently the Ingress only supports a single TLS \
        port, 443. If multiple members of this list specify different hosts, they will \
        be multiplexed on the same port according to the hostname specified through \
        the SNI TLS extension, if the ingress controller fulfilling the ingress \
        supports SNI.
    :type tls: List[IngressTLS]
    :param backend:A default backend capable of servicing requests that don't match \
        any rule. At least one of 'backend' or 'rules' must be specified. This field \
        is optional to allow the loadbalancer controller or defaulting logic to \
        specify a global default.
    :type backend: Optional[IngressBackend]
    """

    def __init__(
        self,
        ingress_class_name: str,
        rules: List[IngressRule],
        tls: List[IngressTLS],
        backend: Optional[IngressBackend] = None,
    ):
        self.ingressClassName = ingress_class_name
        self.rules = rules
        self.tls = tls
        self.backend = backend


class Ingress(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec is the desired state of the Ingress. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: IngressSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: IngressSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class IPBlock(HelmYaml):
    """
    :param cidr:CIDR is a string representing the IP Block Valid examples are \
        "192.168.1.1/24" or "2001:db9::/64"
    :type cidr: str
    :param except_:Except is a slice of CIDRs that should not be included within an IP \
        Block Valid examples are "192.168.1.1/24" or "2001:db9::/64" Except values \
        will be rejected if they are outside the CIDR range
    :type except_: List[str]
    """

    def __init__(self, cidr: str, except_: List[str]):
        self.cidr = cidr
        self["except"] = except_


class NetworkPolicyPeer(HelmYaml):
    """
    :param ip_block:IPBlock defines policy on a particular IPBlock. If this field is \
        set then neither of the other fields can be.
    :type ip_block: IPBlock
    :param namespace_selector:Selects Namespaces using cluster-scoped labels. This \
        field follows standard label selector semantics; if present but empty, it \
        selects all namespaces.  If PodSelector is also set, then the \
        NetworkPolicyPeer as a whole selects the Pods matching PodSelector in the \
        Namespaces selected by NamespaceSelector. Otherwise it selects all Pods in the \
        Namespaces selected by NamespaceSelector.
    :type namespace_selector: LabelSelector
    :param pod_selector:This is a label selector which selects Pods. This field \
        follows standard label selector semantics; if present but empty, it selects \
        all pods.  If NamespaceSelector is also set, then the NetworkPolicyPeer as a \
        whole selects the Pods matching PodSelector in the Namespaces selected by \
        NamespaceSelector. Otherwise it selects the Pods matching PodSelector in the \
        policy's own Namespace.
    :type pod_selector: LabelSelector
    """

    def __init__(
        self,
        ip_block: IPBlock,
        namespace_selector: LabelSelector,
        pod_selector: LabelSelector,
    ):
        self.ipBlock = ip_block
        self.namespaceSelector = namespace_selector
        self.podSelector = pod_selector


class IngressClassSpec(HelmYaml):
    """
    :param controller:Controller refers to the name of the controller that should \
        handle this class. This allows for different "flavors" that are controlled by \
        the same controller. For example, you may have different Parameters for the \
        same implementing controller. This should be specified as a domain-prefixed \
        path no more than 250 characters in length, e.g. "acme.io/ingress-controller". \
        This field is immutable.
    :type controller: str
    :param parameters:Parameters is a link to a custom resource containing additional \
        configuration for the controller. This is optional if the controller does not \
        require extra parameters.
    :type parameters: Optional[TypedLocalObjectReference]
    """

    def __init__(
        self, controller: str, parameters: Optional[TypedLocalObjectReference] = None
    ):
        self.controller = controller
        self.parameters = parameters


class IngressClass(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec is the desired state of the IngressClass. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: IngressClassSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: IngressClassSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class IngressClassList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata.
    :type metadata: ListMeta
    :param items:Items is the list of IngressClasses.
    :type items: List[IngressClass]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[IngressClass],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class NetworkPolicyPort(HelmYaml):
    """
    :param port:The port on the given protocol. This can either be a numerical or \
        named port on a pod. If this field is not provided, this matches all port \
        names and numbers.
    :type port: Optional[str]
    :param protocol:The protocol (TCP, UDP, or SCTP) which traffic must match. If not \
        specified, this field defaults to TCP.
    :type protocol: Optional[str]
    """

    def __init__(self, port: Optional[str] = None, protocol: Optional[str] = None):
        self.port = port
        self.protocol = protocol


class NetworkPolicyIngressRule(HelmYaml):
    """
    :param from_:List of sources which should be able to access the pods selected for \
        this rule. Items in this list are combined using a logical OR operation. If \
        this field is empty or missing, this rule matches all sources (traffic not \
        restricted by source). If this field is present and contains at least one \
        item, this rule allows traffic only if the traffic matches at least one item \
        in the from list.
    :type from_: List[NetworkPolicyPeer]
    :param ports:List of ports which should be made accessible on the pods selected \
        for this rule. Each item in this list is combined using a logical OR. If this \
        field is empty or missing, this rule matches all ports (traffic not restricted \
        by port). If this field is present and contains at least one item, then this \
        rule allows traffic only if the traffic matches at least one port in the list.
    :type ports: List[NetworkPolicyPort]
    """

    def __init__(self, from_: List[NetworkPolicyPeer], ports: List[NetworkPolicyPort]):
        self["from"] = from_
        self.ports = ports


class NetworkPolicyEgressRule(HelmYaml):
    """
    :param ports:List of destination ports for outgoing traffic. Each item in this \
        list is combined using a logical OR. If this field is empty or missing, this \
        rule matches all ports (traffic not restricted by port). If this field is \
        present and contains at least one item, then this rule allows traffic only if \
        the traffic matches at least one port in the list.
    :type ports: List[NetworkPolicyPort]
    :param to:List of destinations for outgoing traffic of pods selected for this \
        rule. Items in this list are combined using a logical OR operation. If this \
        field is empty or missing, this rule matches all destinations (traffic not \
        restricted by destination). If this field is present and contains at least one \
        item, this rule allows traffic only if the traffic matches at least one item \
        in the to list.
    :type to: List[NetworkPolicyPeer]
    """

    def __init__(self, ports: List[NetworkPolicyPort], to: List[NetworkPolicyPeer]):
        self.ports = ports
        self.to = to


class NetworkPolicySpec(HelmYaml):
    """
    :param egress:List of egress rules to be applied to the selected pods. Outgoing \
        traffic is allowed if there are no NetworkPolicies selecting the pod (and \
        cluster policy otherwise allows the traffic), OR if the traffic matches at \
        least one egress rule across all of the NetworkPolicy objects whose \
        podSelector matches the pod. If this field is empty then this NetworkPolicy \
        limits all outgoing traffic (and serves solely to ensure that the pods it \
        selects are isolated by default). This field is beta-level in 1.8
    :type egress: List[NetworkPolicyEgressRule]
    :param ingress:List of ingress rules to be applied to the selected pods. Traffic \
        is allowed to a pod if there are no NetworkPolicies selecting the pod (and \
        cluster policy otherwise allows the traffic), OR if the traffic source is the \
        pod's local node, OR if the traffic matches at least one ingress rule across \
        all of the NetworkPolicy objects whose podSelector matches the pod. If this \
        field is empty then this NetworkPolicy does not allow any traffic (and serves \
        solely to ensure that the pods it selects are isolated by default)
    :type ingress: List[NetworkPolicyIngressRule]
    :param pod_selector:Selects the pods to which this NetworkPolicy object applies. \
        The array of ingress rules is applied to any pods selected by this field. \
        Multiple network policies can select the same set of pods. In this case, the \
        ingress rules for each are combined additively. This field is NOT optional and \
        follows standard label selector semantics. An empty podSelector matches all \
        pods in this namespace.
    :type pod_selector: LabelSelector
    :param policy_types:List of rule types that the NetworkPolicy relates to. Valid \
        options are "Ingress", "Egress", or "Ingress,Egress". If this field is not \
        specified, it will default based on the existence of Ingress or Egress rules; \
        policies that contain an Egress section are assumed to affect Egress, and all \
        policies (whether or not they contain an Ingress section) are assumed to \
        affect Ingress. If you want to write an egress-only policy, you must \
        explicitly specify policyTypes [ "Egress" ]. Likewise, if you want to write a \
        policy that specifies that no egress is allowed, you must specify a \
        policyTypes value that include "Egress" (since such a policy would not include \
        an Egress section and would otherwise default to just [ "Ingress" ]). This \
        field is beta-level in 1.8
    :type policy_types: List[str]
    """

    def __init__(
        self,
        egress: List[NetworkPolicyEgressRule],
        ingress: List[NetworkPolicyIngressRule],
        pod_selector: LabelSelector,
        policy_types: List[str],
    ):
        self.egress = egress
        self.ingress = ingress
        self.podSelector = pod_selector
        self.policyTypes = policy_types


class NetworkPolicy(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the desired behavior for this NetworkPolicy.
    :type spec: NetworkPolicySpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: NetworkPolicySpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class NetworkPolicyList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param items:Items is a list of schema objects.
    :type items: List[NetworkPolicy]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[NetworkPolicy],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items
