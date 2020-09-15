"""
Classes related to networking (NetworkPolicy and IngressClass)
"""

from typing import List, Optional

from avionix.kube.base_objects import Networking
from avionix.kube.core import TypedLocalObjectReference
from avionix.kube.meta import LabelSelector, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class IPBlock(HelmYaml):
    """
    :param cidr: CIDR is a string representing the IP Block Valid examples are \
        "192.168.1.1/24" or "2001:db9::/64"
    :param except_: Except is a slice of CIDRs that should not be included within an IP \
        Block Valid examples are "192.168.1.1/24" or "2001:db9::/64" Except values \
        will be rejected if they are outside the CIDR range
    """

    def __init__(self, cidr: str, except_: Optional[List[str]] = None):
        self.cidr = cidr
        self["except"] = except_


class NetworkPolicyPeer(HelmYaml):
    """
    :param ip_block: IPBlock defines policy on a particular IPBlock. If this field is \
        set then neither of the other fields can be.
    :param namespace_selector: Selects Namespaces using cluster-scoped labels. This \
        field follows standard label selector semantics; if present but empty, it \
        selects all namespaces.  If PodSelector is also set, then the \
        NetworkPolicyPeer as a whole selects the Pods matching PodSelector in the \
        Namespaces selected by NamespaceSelector. Otherwise it selects all Pods in the \
        Namespaces selected by NamespaceSelector.
    :param pod_selector: This is a label selector which selects Pods. This field \
        follows standard label selector semantics; if present but empty, it selects \
        all pods.  If NamespaceSelector is also set, then the NetworkPolicyPeer as a \
        whole selects the Pods matching PodSelector in the Namespaces selected by \
        NamespaceSelector. Otherwise it selects the Pods matching PodSelector in the \
        policy's own Namespace.
    """

    def __init__(
        self,
        ip_block: IPBlock,
        namespace_selector: Optional[LabelSelector] = None,
        pod_selector: Optional[LabelSelector] = None,
    ):
        self.ipBlock = ip_block
        self.namespaceSelector = namespace_selector
        self.podSelector = pod_selector


class NetworkPolicyPort(HelmYaml):
    """
    :param port: The port on the given protocol. This can either be a numerical or \
        named port on a pod. If this field is not provided, this matches all port \
        names and numbers.
    :param protocol: The protocol (TCP, UDP, or SCTP) which traffic must match. If not \
        specified, this field defaults to TCP.
    """

    def __init__(self, port: Optional[int] = None, protocol: Optional[str] = None):
        self.port = port
        self.protocol = protocol


class NetworkPolicyIngressRule(HelmYaml):
    """
    :param from_: List of sources which should be able to access the pods selected for \
        this rule. Items in this list are combined using a logical OR operation. If \
        this field is empty or missing, this rule matches all sources (traffic not \
        restricted by source). If this field is present and contains at least one \
        item, this rule allows traffic only if the traffic matches at least one item \
        in the from list.
    :param ports: List of ports which should be made accessible on the pods selected \
        for this rule. Each item in this list is combined using a logical OR. If this \
        field is empty or missing, this rule matches all ports (traffic not restricted \
        by port). If this field is present and contains at least one item, then this \
        rule allows traffic only if the traffic matches at least one port in the list.
    """

    def __init__(self, from_: List[NetworkPolicyPeer], ports: List[NetworkPolicyPort]):
        self["from"] = from_
        self.ports = ports


class NetworkPolicyEgressRule(HelmYaml):
    """
    :param ports: List of destination ports for outgoing traffic. Each item in this \
        list is combined using a logical OR. If this field is empty or missing, this \
        rule matches all ports (traffic not restricted by port). If this field is \
        present and contains at least one item, then this rule allows traffic only if \
        the traffic matches at least one port in the list.
    :param to: List of destinations for outgoing traffic of pods selected for this \
        rule. Items in this list are combined using a logical OR operation. If this \
        field is empty or missing, this rule matches all destinations (traffic not \
        restricted by destination). If this field is present and contains at least one \
        item, this rule allows traffic only if the traffic matches at least one item \
        in the to list.
    """

    def __init__(self, ports: List[NetworkPolicyPort], to: List[NetworkPolicyPeer]):
        self.ports = ports
        self.to = to


class NetworkPolicySpec(HelmYaml):
    """
    :param egress: List of egress rules to be applied to the selected pods. Outgoing \
        traffic is allowed if there are no NetworkPolicies selecting the pod (and \
        cluster policy otherwise allows the traffic), OR if the traffic matches at \
        least one egress rule across all of the NetworkPolicy objects whose \
        podSelector matches the pod. If this field is empty then this NetworkPolicy \
        limits all outgoing traffic (and serves solely to ensure that the pods it \
        selects are isolated by default). This field is beta-level in 1.8
    :param ingress: List of ingress rules to be applied to the selected pods. Traffic \
        is allowed to a pod if there are no NetworkPolicies selecting the pod (and \
        cluster policy otherwise allows the traffic), OR if the traffic source is the \
        pod's local node, OR if the traffic matches at least one ingress rule across \
        all of the NetworkPolicy objects whose podSelector matches the pod. If this \
        field is empty then this NetworkPolicy does not allow any traffic (and serves \
        solely to ensure that the pods it selects are isolated by default)
    :param pod_selector: Selects the pods to which this NetworkPolicy object applies. \
        The array of ingress rules is applied to any pods selected by this field. \
        Multiple network policies can select the same set of pods. In this case, the \
        ingress rules for each are combined additively. This field is NOT optional and \
        follows standard label selector semantics. An empty podSelector matches all \
        pods in this namespace.
    :param policy_types: List of rule types that the NetworkPolicy relates to. Valid \
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
    """

    def __init__(
        self,
        egress: Optional[List[NetworkPolicyEgressRule]],
        ingress: Optional[List[NetworkPolicyIngressRule]],
        pod_selector: Optional[LabelSelector],
        policy_types: Optional[List[str]],
    ):
        self.egress = egress
        self.ingress = ingress
        self.podSelector = pod_selector
        self.policyTypes = policy_types


class NetworkPolicy(Networking):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: Specification of the desired behavior for this NetworkPolicy.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
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


class IngressClassSpec(HelmYaml):
    """
    :param controller: Controller refers to the name of the controller that should \
        handle this class. This allows for different "flavors" that are controlled by \
        the same controller. For example, you may have different Parameters for the \
        same implementing controller. This should be specified as a domain-prefixed \
        path no more than 250 characters in length, e.g. "acme.io/ingress-controller". \
        This field is immutable.
    :param parameters: Parameters is a link to a custom resource containing additional \
        configuration for the controller. This is optional if the controller does not \
        require extra parameters.
    """

    def __init__(
        self, controller: str, parameters: Optional[TypedLocalObjectReference] = None
    ):
        self.controller = controller
        self.parameters = parameters


class IngressClass(Networking):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: Spec is the desired state of the IngressClass. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    _non_standard_version = "v1beta1"

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: IngressClassSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec
