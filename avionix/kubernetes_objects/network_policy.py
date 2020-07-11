from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.selector import LabelSelector
from avionix.yaml.yaml_handling import HelmYaml


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


class NetworkPolicyEgressRule(HelmYaml):
    """
    :param to:List of destinations for outgoing traffic of pods selected for this \
        rule. Items in this list are combined using a logical OR operation. If this \
        field is empty or missing, this rule matches all destinations (traffic not \
        restricted by destination). If this field is present and contains at least one \
        item, this rule allows traffic only if the traffic matches at least one item \
        in the to list.
    :type to: List[NetworkPolicyPeer]
    :param ports:List of destination ports for outgoing traffic. Each item in this \
        list is combined using a logical OR. If this field is empty or missing, this \
        rule matches all ports (traffic not restricted by port). If this field is \
        present and contains at least one item, then this rule allows traffic only if \
        the traffic matches at least one port in the list.
    :type ports: Optional[List[NetworkPolicyPort]]
    """

    def __init__(
        self,
        to: List[NetworkPolicyPeer],
        ports: Optional[List[NetworkPolicyPort]] = None,
    ):
        self.to = to
        self.ports = ports


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
    :type ports: Optional[List[NetworkPolicyPort]]
    """

    def __init__(
        self,
        from_: List[NetworkPolicyPeer],
        ports: Optional[List[NetworkPolicyPort]] = None,
    ):
        self["from"] = from_
        self.ports = ports


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
    :param items:Items is a list of schema objects.
    :type items: List[NetworkPolicy]
    :param metadata:Standard list metadata. More info: \
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
        items: List[NetworkPolicy],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
