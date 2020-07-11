from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class NodeSelectorRequirement(HelmYaml):
    """
    :param key:The label key that the selector applies to.
    :type key: str
    :param operator:Represents a key's relationship to a set of values. Valid \
        operators are In, NotIn, Exists, DoesNotExist. Gt, and Lt.
    :type operator: str
    :param values:An array of string values. If the operator is In or NotIn, the \
        values array must be non-empty. If the operator is Exists or DoesNotExist, the \
        values array must be empty. If the operator is Gt or Lt, the values array must \
        have a single element, which will be interpreted as an integer. This array is \
        replaced during a strategic merge patch.
    :type values: List[str]
    """

    def __init__(self, key: str, operator: str, values: List[str]):
        self.key = key
        self.operator = operator
        self.values = values


class NodeSelectorTerm(HelmYaml):
    """
    :param match_expressions:A list of node selector requirements by node's labels.
    :type match_expressions: List[NodeSelectorRequirement]
    :param match_fields:A list of node selector requirements by node's fields.
    :type match_fields: List[NodeSelectorRequirement]
    """

    def __init__(
        self,
        match_expressions: List[NodeSelectorRequirement],
        match_fields: List[NodeSelectorRequirement],
    ):
        self.matchExpressions = match_expressions
        self.matchFields = match_fields


class NodeSelector(HelmYaml):
    """
    :param node_selector_terms:Required. A list of node selector terms. The terms are \
        ORed.
    :type node_selector_terms: List[NodeSelectorTerm]
    """

    def __init__(self, node_selector_terms: List[NodeSelectorTerm]):
        self.nodeSelectorTerms = node_selector_terms


class PreferredSchedulingTerm(HelmYaml):
    """
    :param preference:A node selector term, associated with the corresponding weight.
    :type preference: NodeSelectorTerm
    :param weight:Weight associated with matching the corresponding nodeSelectorTerm, \
        in the range 1-100.
    :type weight: int
    """

    def __init__(self, preference: NodeSelectorTerm, weight: int):
        self.preference = preference
        self.weight = weight


class NodeAffinity(HelmYaml):
    """
    :param preferred_during_scheduling_ignored_during_execution:The scheduler will \
        prefer to schedule pods to nodes that satisfy the affinity expressions \
        specified by this field, but it may choose a node that violates one or more of \
        the expressions. The node that is most preferred is the one with the greatest \
        sum of weights, i.e. for each node that meets all of the scheduling \
        requirements (resource request, requiredDuringScheduling affinity expressions, \
        etc.), compute a sum by iterating through the elements of this field and \
        adding "weight" to the sum if the node matches the corresponding \
        matchExpressions; the node(s) with the highest sum are the most preferred.
    :type preferred_during_scheduling_ignored_during_execution: List[PreferredSchedulingTerm]
    :param required_during_scheduling_ignored_during_execution:If the affinity \
        requirements specified by this field are not met at scheduling time, the pod \
        will not be scheduled onto the node. If the affinity requirements specified by \
        this field cease to be met at some point during pod execution (e.g. due to an \
        update), the system may or may not try to eventually evict the pod from its \
        node.
    :type required_during_scheduling_ignored_during_execution: NodeSelector
    """

    def __init__(
        self,
        preferred_during_scheduling_ignored_during_execution: List[
            PreferredSchedulingTerm
        ],
        required_during_scheduling_ignored_during_execution: NodeSelector,
    ):
        self.preferredDuringSchedulingIgnoredDuringExecution = (
            preferred_during_scheduling_ignored_during_execution
        )
        self.requiredDuringSchedulingIgnoredDuringExecution = (
            required_during_scheduling_ignored_during_execution
        )


class NodeAddress(HelmYaml):
    """
    :param address:The node address.
    :type address: str
    :param type:Node address type, one of Hostname, ExternalIP or InternalIP.
    :type type: str
    """

    def __init__(self, address: str, type: str):
        self.address = address
        self.type = type


class ConfigMapNodeConfigSource(HelmYaml):
    """
    :param kubelet_config_key:KubeletConfigKey declares which key of the referenced \
        ConfigMap corresponds to the KubeletConfiguration structure This field is \
        required in all cases.
    :type kubelet_config_key: str
    :param resource_version:ResourceVersion is the metadata.ResourceVersion of the \
        referenced ConfigMap. This field is forbidden in Node.Spec, and required in \
        Node.Status.
    :type resource_version: str
    :param uid:UID is the metadata.UID of the referenced ConfigMap. This field is \
        forbidden in Node.Spec, and required in Node.Status.
    :type uid: str
    :param name:Name is the metadata.name of the referenced ConfigMap. This field is \
        required in all cases.
    :type name: Optional[str]
    :param namespace:Namespace is the metadata.namespace of the referenced ConfigMap. \
        This field is required in all cases.
    :type namespace: Optional[str]
    """

    def __init__(
        self,
        kubelet_config_key: str,
        resource_version: str,
        uid: str,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        self.kubeletConfigKey = kubelet_config_key
        self.resourceVersion = resource_version
        self.uid = uid
        self.name = name
        self.namespace = namespace


class NodeConfigSource(HelmYaml):
    """
    :param config_map:ConfigMap is a reference to a Node's ConfigMap
    :type config_map: ConfigMapNodeConfigSource
    """

    def __init__(self, config_map: ConfigMapNodeConfigSource):
        self.configMap = config_map


class DaemonEndpoint(HelmYaml):
    """
    :param port:Port number of the given endpoint.
    :type port: int
    """

    def __init__(self, port: int):
        self.Port = port


class NodeDaemonEndpoints(HelmYaml):
    """
    :param kubelet_endpoint:Endpoint on which Kubelet is listening.
    :type kubelet_endpoint: DaemonEndpoint
    """

    def __init__(self, kubelet_endpoint: DaemonEndpoint):
        self.kubeletEndpoint = kubelet_endpoint


class NodeSystemInfo(HelmYaml):
    """
    :param architecture:The Architecture reported by the node
    :type architecture: str
    :param boot_id:Boot ID reported by the node.
    :type boot_id: str
    :param container_runtime_version:ContainerRuntime Version reported by the node \
        through runtime remote API (e.g. docker://1.5.0).
    :type container_runtime_version: str
    :param kernel_version:Kernel Version reported by the node from 'uname -r' (e.g. \
        3.16.0-0.bpo.4-amd64).
    :type kernel_version: str
    :param kube_proxy_version:KubeProxy Version reported by the node.
    :type kube_proxy_version: str
    :param kubelet_version:Kubelet Version reported by the node.
    :type kubelet_version: str
    :param machine_id:MachineID reported by the node. For unique machine \
        identification in the cluster this field is preferred. Learn more from man(5) \
        machine-id: http://man7.org/linux/man-pages/man5/machine-id.5.html
    :type machine_id: str
    :param operating_system:The Operating System reported by the node
    :type operating_system: str
    :param os_image:OS Image reported by the node from /etc/os-release (e.g. Debian \
        GNU/Linux 7 (wheezy)).
    :type os_image: str
    :param system_uuid:SystemUUID reported by the node. For unique machine \
        identification MachineID is preferred. This field is specific to Red Hat hosts \
        https://access.redhat.com/documentation/en-US/Red_Hat_Subscription_Management/1/html/RHSM/getting-system-uuid.html  # noqa
    :type system_uuid: str
    """

    def __init__(
        self,
        architecture: str,
        boot_id: str,
        container_runtime_version: str,
        kernel_version: str,
        kube_proxy_version: str,
        kubelet_version: str,
        machine_id: str,
        operating_system: str,
        os_image: str,
        system_uuid: str,
    ):
        self.architecture = architecture
        self.bootID = boot_id
        self.containerRuntimeVersion = container_runtime_version
        self.kernelVersion = kernel_version
        self.kubeProxyVersion = kube_proxy_version
        self.kubeletVersion = kubelet_version
        self.machineID = machine_id
        self.operatingSystem = operating_system
        self.osImage = os_image
        self.systemUUID = system_uuid


class NodeCondition(HelmYaml):
    """
    :param last_heartbeat_time:Last time we got an update on a given condition.
    :type last_heartbeat_time: time
    :param last_transition_time:Last time the condition transit from one status to \
        another.
    :type last_transition_time: time
    :param message:Human readable message indicating details about last transition.
    :type message: str
    :param reason:(brief) reason for the condition's last transition.
    :type reason: str
    :param type:Type of node condition.
    :type type: str
    """

    def __init__(
        self,
        last_heartbeat_time: time,
        last_transition_time: time,
        message: str,
        reason: str,
        type: str,
    ):
        self.lastHeartbeatTime = last_heartbeat_time
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class VolumeNodeAffinity(HelmYaml):
    """
    :param required:Required specifies hard node constraints that must be met.
    :type required: NodeSelector
    """

    def __init__(self, required: NodeSelector):
        self.required = required


class Taint(HelmYaml):
    """
    :param effect:Required. The effect of the taint on pods that do not tolerate the \
        taint. Valid effects are NoSchedule, PreferNoSchedule and NoExecute.
    :type effect: str
    :param key:Required. The taint key to be applied to a node.
    :type key: str
    :param time_added:TimeAdded represents the time at which the taint was added. It \
        is only written for NoExecute taints.
    :type time_added: time
    :param value:The taint value corresponding to the taint key.
    :type value: str
    """

    def __init__(self, effect: str, key: str, time_added: time, value: str):
        self.effect = effect
        self.key = key
        self.timeAdded = time_added
        self.value = value


class NodeSpec(HelmYaml):
    """
    :param external_id:Deprecated. Not all kubelets will set this field. Remove field \
        after 1.13. see: https://issues.k8s.io/61966
    :type external_id: str
    :param pod_cidr:PodCIDR represents the pod IP range assigned to the node.
    :type pod_cidr: str
    :param pod_cidrs:podCIDRs represents the IP ranges assigned to the node for usage \
        by Pods on that node. If this field is specified, the 0th entry must match the \
        podCIDR field. It may contain at most 1 value for each of IPv4 and IPv6.
    :type pod_cidrs: List[str]
    :param provider_id:ID of the node assigned by the cloud provider in the format: \
        <ProviderName>://<ProviderSpecificNodeID>
    :type provider_id: str
    :param unschedulable:Unschedulable controls node schedulability of new pods. By \
        default, node is schedulable. More info: \
        https://kubernetes.io/docs/concepts/nodes/node/#manual-node-administration
    :type unschedulable: bool
    :param config_source:If specified, the source to get node configuration from The \
        DynamicKubeletConfig feature gate must be enabled for the Kubelet to use this \
        field
    :type config_source: Optional[NodeConfigSource]
    :param taints:If specified, the node's taints.
    :type taints: Optional[List[Taint]]
    """

    def __init__(
        self,
        external_id: str,
        pod_cidr: str,
        pod_cidrs: List[str],
        provider_id: str,
        unschedulable: bool,
        config_source: Optional[NodeConfigSource] = None,
        taints: Optional[List[Taint]] = None,
    ):
        self.externalID = external_id
        self.podCIDR = pod_cidr
        self.podCIDRs = pod_cidrs
        self.providerID = provider_id
        self.unschedulable = unschedulable
        self.configSource = config_source
        self.taints = taints


class Node(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the behavior of a node. \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: NodeSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: NodeSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class NodeList(KubernetesBaseObject):
    """
    :param items:List of nodes
    :type items: List[Node]
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
        self, items: List[Node], metadata: ListMeta, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
