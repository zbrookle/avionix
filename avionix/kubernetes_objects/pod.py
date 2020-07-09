from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.container import Container, EphemeralContainer
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.node import NodeAffinity
from avionix.kubernetes_objects.reference import (
    CrossVersionObjectReference,
    LocalObjectReference,
)
from avionix.kubernetes_objects.security import (
    SELinuxOptions,
    WindowsSecurityContextOptions,
)
from avionix.kubernetes_objects.selector import LabelSelector
from avionix.kubernetes_objects.topology import TopologySpreadConstraint
from avionix.kubernetes_objects.volume import Volume
from avionix.yaml.yaml_handling import HelmYaml


class HorizontalPodAutoscalerSpec(HelmYaml):
    """
    :param max_replicas:upper limit for the number of pods that can be set by the \
        autoscaler; cannot be smaller than MinReplicas.
    :type max_replicas: int
    :param scale_target_ref:reference to scaled resource; horizontal pod autoscaler \
        will learn the current resource consumption and will set the desired number of \
        pods by using its Scale subresource.
    :type scale_target_ref: CrossVersionObjectReference
    :param min_replicas:minReplicas is the lower limit for the number of replicas to \
        which the autoscaler can scale down.  It defaults to 1 pod.  minReplicas is \
        allowed to be 0 if the alpha feature gate HPAScaleToZero is enabled and at \
        least one Object or External metric is configured.  Scaling is active as long \
        as at least one metric value is available.
    :type min_replicas: Optional[int]
    :param target_cpuutilization_percentage:target average CPU utilization \
        (represented as a percentage of requested CPU) over all the pods; if not \
        specified the default autoscaling policy will be used.
    :type target_cpuutilization_percentage: Optional[int]
    """

    def __init__(
        self,
        max_replicas: int,
        scale_target_ref: CrossVersionObjectReference,
        min_replicas: Optional[int] = None,
        target_cpuutilization_percentage: Optional[int] = None,
    ):
        self.maxReplicas = max_replicas
        self.scaleTargetRef = scale_target_ref
        self.minReplicas = min_replicas
        self.targetCPUUtilizationPercentage = target_cpuutilization_percentage


class HorizontalPodAutoscaler(KubernetesBaseObject):
    """
    :param metadata:Standard object metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:behaviour of autoscaler. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.  # noqa
    :type spec: HorizontalPodAutoscalerSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: HorizontalPodAutoscalerSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class HorizontalPodAutoscalerList(KubernetesBaseObject):
    """
    :param items:list of horizontal pod autoscaler objects.
    :type items: List[HorizontalPodAutoscaler]
    :param metadata:Standard list metadata.
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[HorizontalPodAutoscaler],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class Toleration(HelmYaml):
    """
    :param effect:Effect indicates the taint effect to match. Empty means match all \
        taint effects. When specified, allowed values are NoSchedule, PreferNoSchedule \
        and NoExecute.
    :type effect: str
    :param key:Key is the taint key that the toleration applies to. Empty means match \
        all taint keys. If the key is empty, operator must be Exists; this combination \
        means to match all values and all keys.
    :type key: str
    :param toleration_seconds:TolerationSeconds represents the period of time the \
        toleration (which must be of effect NoExecute, otherwise this field is \
        ignored) tolerates the taint. By default, it is not set, which means tolerate \
        the taint forever (do not evict). Zero and negative values will be treated as \
        0 (evict immediately) by the system.
    :type toleration_seconds: int
    :param value:Value is the taint value the toleration matches to. If the operator \
        is Exists, the value should be empty, otherwise just a regular string.
    :type value: str
    :param operator:Operator represents a key's relationship to the value. Valid \
        operators are Exists and Equal. Defaults to Equal. Exists is equivalent to \
        wildcard for value, so that a pod can tolerate all taints of a particular \
        category.
    :type operator: Optional[str]
    """

    def __init__(
        self,
        effect: str,
        key: str,
        toleration_seconds: int,
        value: str,
        operator: Optional[str] = None,
    ):
        self.effect = effect
        self.key = key
        self.tolerationSeconds = toleration_seconds
        self.value = value
        self.operator = operator


class PodAffinityTerm(HelmYaml):
    """
    :param label_selector:A label query over a set of resources, in this case pods.
    :type label_selector: LabelSelector
    :param namespaces:namespaces specifies which namespaces the labelSelector applies \
        to (matches against); null or empty list means "this pod's namespace"
    :type namespaces: List[str]
    :param topology_key:This pod should be co-located (affinity) or not co-located \
        (anti-affinity) with the pods matching the labelSelector in the specified \
        namespaces, where co-located is defined as running on a node whose value of \
        the label with key topologyKey matches that of any node on which any of the \
        selected pods is running. Empty topologyKey is not allowed.
    :type topology_key: str
    """

    def __init__(
        self, label_selector: LabelSelector, namespaces: List[str], topology_key: str
    ):
        self.labelSelector = label_selector
        self.namespaces = namespaces
        self.topologyKey = topology_key


class WeightedPodAffinityTerm(HelmYaml):
    """
    :param pod_affinity_term:Required. A pod affinity term, associated with the \
        corresponding weight.
    :type pod_affinity_term: PodAffinityTerm
    :param weight:weight associated with matching the corresponding podAffinityTerm, \
        in the range 1-100.
    :type weight: int
    """

    def __init__(self, pod_affinity_term: PodAffinityTerm, weight: int):
        self.podAffinityTerm = pod_affinity_term
        self.weight = weight


class PodAntiAffinity(HelmYaml):
    """
    :param preferred_during_scheduling_ignored_during_execution:The scheduler will \
        prefer to schedule pods to nodes that satisfy the anti-affinity expressions \
        specified by this field, but it may choose a node that violates one or more of \
        the expressions. The node that is most preferred is the one with the greatest \
        sum of weights, i.e. for each node that meets all of the scheduling \
        requirements (resource request, requiredDuringScheduling anti-affinity \
        expressions, etc.), compute a sum by iterating through the elements of this \
        field and adding "weight" to the sum if the node has pods which matches the \
        corresponding podAffinityTerm; the node(s) with the highest sum are the most \
        preferred.
    :type preferred_during_scheduling_ignored_during_execution: List[WeightedPodAffinityTerm]
    :param required_during_scheduling_ignored_during_execution:If the anti-affinity \
        requirements specified by this field are not met at scheduling time, the pod \
        will not be scheduled onto the node. If the anti-affinity requirements \
        specified by this field cease to be met at some point during pod execution \
        (e.g. due to a pod label update), the system may or may not try to eventually \
        evict the pod from its node. When there are multiple elements, the lists of \
        nodes corresponding to each podAffinityTerm are intersected, i.e. all terms \
        must be satisfied.
    :type required_during_scheduling_ignored_during_execution: List[PodAffinityTerm]
    """

    def __init__(
        self,
        preferred_during_scheduling_ignored_during_execution: List[
            WeightedPodAffinityTerm
        ],
        required_during_scheduling_ignored_during_execution: List[PodAffinityTerm],
    ):
        self.preferredDuringSchedulingIgnoredDuringExecution = (
            preferred_during_scheduling_ignored_during_execution
        )
        self.requiredDuringSchedulingIgnoredDuringExecution = (
            required_during_scheduling_ignored_during_execution
        )


class PodAffinity(HelmYaml):
    """
    :param preferred_during_scheduling_ignored_during_execution:The scheduler will \
        prefer to schedule pods to nodes that satisfy the affinity expressions \
        specified by this field, but it may choose a node that violates one or more of \
        the expressions. The node that is most preferred is the one with the greatest \
        sum of weights, i.e. for each node that meets all of the scheduling \
        requirements (resource request, requiredDuringScheduling affinity expressions, \
        etc.), compute a sum by iterating through the elements of this field and \
        adding "weight" to the sum if the node has pods which matches the \
        corresponding podAffinityTerm; the node(s) with the highest sum are the most \
        preferred.
    :type preferred_during_scheduling_ignored_during_execution: List[WeightedPodAffinityTerm]
    :param required_during_scheduling_ignored_during_execution:If the affinity \
        requirements specified by this field are not met at scheduling time, the pod \
        will not be scheduled onto the node. If the affinity requirements specified by \
        this field cease to be met at some point during pod execution (e.g. due to a \
        pod label update), the system may or may not try to eventually evict the pod \
        from its node. When there are multiple elements, the lists of nodes \
        corresponding to each podAffinityTerm are intersected, i.e. all terms must be \
        satisfied.
    :type required_during_scheduling_ignored_during_execution: List[PodAffinityTerm]
    """

    def __init__(
        self,
        preferred_during_scheduling_ignored_during_execution: List[
            WeightedPodAffinityTerm
        ],
        required_during_scheduling_ignored_during_execution: List[PodAffinityTerm],
    ):
        self.preferredDuringSchedulingIgnoredDuringExecution = (
            preferred_during_scheduling_ignored_during_execution
        )
        self.requiredDuringSchedulingIgnoredDuringExecution = (
            required_during_scheduling_ignored_during_execution
        )


class Affinity(HelmYaml):
    """
    :param node_affinity:Describes node affinity scheduling rules for the pod.
    :type node_affinity: NodeAffinity
    :param pod_affinity:Describes pod affinity scheduling rules (e.g. co-locate this \
        pod in the same node, zone, etc. as some other pod(s)).
    :type pod_affinity: PodAffinity
    :param pod_anti_affinity:Describes pod anti-affinity scheduling rules (e.g. avoid \
        putting this pod in the same node, zone, etc. as some other pod(s)).
    :type pod_anti_affinity: PodAntiAffinity
    """

    def __init__(
        self,
        node_affinity: NodeAffinity,
        pod_affinity: PodAffinity,
        pod_anti_affinity: PodAntiAffinity,
    ):
        self.nodeAffinity = node_affinity
        self.podAffinity = pod_affinity
        self.podAntiAffinity = pod_anti_affinity


class PodDNSConfigOption(HelmYaml):
    """
    :param value:None
    :type value: str
    :param name:Required.
    :type name: Optional[str]
    """

    def __init__(self, value: str, name: Optional[str] = None):
        self.value = value
        self.name = name


class PodDNSConfig(HelmYaml):
    """
    :param nameservers:A list of DNS name server IP addresses. This will be appended \
        to the base nameservers generated from DNSPolicy. Duplicated nameservers will \
        be removed.
    :type nameservers: List[str]
    :param options:A list of DNS resolver options. This will be merged with the base \
        options generated from DNSPolicy. Duplicated entries will be removed. \
        Resolution options given in Options will override those that appear in the \
        base DNSPolicy.
    :type options: List[PodDNSConfigOption]
    :param searches:A list of DNS search domains for host-name lookup. This will be \
        appended to the base search paths generated from DNSPolicy. Duplicated search \
        paths will be removed.
    :type searches: List[str]
    """

    def __init__(
        self,
        nameservers: List[str],
        options: List[PodDNSConfigOption],
        searches: List[str],
    ):
        self.nameservers = nameservers
        self.options = options
        self.searches = searches


class PodReadinessGate(HelmYaml):
    """
    :param condition_type:ConditionType refers to a condition in the pod's condition \
        list with matching type.
    :type condition_type: str
    """

    def __init__(self, condition_type: str):
        self.conditionType = condition_type


class HostAlias(HelmYaml):
    """
    :param hostnames:Hostnames for the above IP address.
    :type hostnames: List[str]
    :param ip:IP address of the host file entry.
    :type ip: str
    """

    def __init__(self, hostnames: List[str], ip: str):
        self.hostnames = hostnames
        self.ip = ip


class Sysctl(HelmYaml):
    """
    :param value:Value of a property to set
    :type value: str
    :param name:Name of a property to set
    :type name: Optional[str]
    """

    def __init__(self, value: str, name: Optional[str] = None):
        self.value = value
        self.name = name


class PodSecurityContext(HelmYaml):
    """
    :param fs_group:A special supplemental group that applies to all containers in a \
        pod. Some volume types allow the Kubelet to change the ownership of that \
        volume to be owned by the pod:  1. The owning GID will be the FSGroup 2. The \
        setgid bit is set (new files created in the volume will be owned by FSGroup) \
        3. The permission bits are OR'd with rw-rw----  If unset, the Kubelet will not \
        modify the ownership and permissions of any volume.
    :type fs_group: int
    :param run_as_group:The GID to run the entrypoint of the container process. Uses \
        runtime default if unset. May also be set in SecurityContext.  If set in both \
        SecurityContext and PodSecurityContext, the value specified in SecurityContext \
        takes precedence for that container.
    :type run_as_group: int
    :param run_as_non_root:Indicates that the container must run as a non-root user. \
        If true, the Kubelet will validate the image at runtime to ensure that it does \
        not run as UID 0 (root) and fail to start the container if it does. If unset \
        or false, no such validation will be performed. May also be set in \
        SecurityContext.  If set in both SecurityContext and PodSecurityContext, the \
        value specified in SecurityContext takes precedence.
    :type run_as_non_root: bool
    :param se_linux_options:The SELinux context to be applied to all containers. If \
        unspecified, the container runtime will allocate a random SELinux context for \
        each container.  May also be set in SecurityContext.  If set in both \
        SecurityContext and PodSecurityContext, the value specified in SecurityContext \
        takes precedence for that container.
    :type se_linux_options: SELinuxOptions
    :param supplemental_groups:A list of groups applied to the first process run in \
        each container, in addition to the container's primary GID.  If unspecified, \
        no groups will be added to any container.
    :type supplemental_groups: List[int]
    :param sysctls:Sysctls hold a list of namespaced sysctls used for the pod. Pods \
        with unsupported sysctls (by the container runtime) might fail to launch.
    :type sysctls: List[Sysctl]
    :param windows_options:The Windows specific settings applied to all containers. If \
        unspecified, the options within a container's SecurityContext will be used. If \
        set in both SecurityContext and PodSecurityContext, the value specified in \
        SecurityContext takes precedence.
    :type windows_options: WindowsSecurityContextOptions
    :param fs_group_change_policy:fsGroupChangePolicy defines behavior of changing \
        ownership and permission of the volume before being exposed inside Pod. This \
        field will only apply to volume types which support fsGroup based \
        ownership(and permissions). It will have no effect on ephemeral volume types \
        such as: secret, configmaps and emptydir. Valid values are "OnRootMismatch" \
        and "Always". If not specified defaults to "Always".
    :type fs_group_change_policy: Optional[str]
    :param run_as_user:The UID to run the entrypoint of the container process. \
        Defaults to user specified in image metadata if unspecified. May also be set \
        in SecurityContext.  If set in both SecurityContext and PodSecurityContext, \
        the value specified in SecurityContext takes precedence for that container.
    :type run_as_user: Optional[int]
    """

    def __init__(
        self,
        fs_group: int,
        run_as_group: int,
        run_as_non_root: bool,
        se_linux_options: SELinuxOptions,
        supplemental_groups: List[int],
        sysctls: List[Sysctl],
        windows_options: WindowsSecurityContextOptions,
        fs_group_change_policy: Optional[str] = None,
        run_as_user: Optional[int] = None,
    ):
        self.fsGroup = fs_group
        self.runAsGroup = run_as_group
        self.runAsNonRoot = run_as_non_root
        self.seLinuxOptions = se_linux_options
        self.supplementalGroups = supplemental_groups
        self.sysctls = sysctls
        self.windowsOptions = windows_options
        self.fsGroupChangePolicy = fs_group_change_policy
        self.runAsUser = run_as_user


class PodSpec(HelmYaml):
    """
    :param containers:List of containers belonging to the pod. Containers cannot \
        currently be added or removed. There must be at least one container in a Pod. \
        Cannot be updated.
    :type containers: List[Container]
    :param active_deadline_seconds:Optional duration in seconds the pod may be active \
        on the node relative to StartTime before the system will actively try to mark \
        it failed and kill associated containers. Value must be a positive integer.
    :type active_deadline_seconds: Optional[int]
    :param affinity:If specified, the pod's scheduling constraints
    :type affinity: Optional[Affinity]
    :param automount_service_account_token:AutomountServiceAccountToken indicates \
        whether a service account token should be automatically mounted.
    :type automount_service_account_token: Optional[bool]
    :param dns_config:Specifies the DNS parameters of a pod. Parameters specified here \
        will be merged to the generated DNS configuration based on DNSPolicy.
    :type dns_config: Optional[PodDNSConfig]
    :param dns_policy:Set DNS policy for the pod. Defaults to "ClusterFirst". Valid \
        values are 'ClusterFirstWithHostNet', 'ClusterFirst', 'Default' or 'None'. DNS \
        parameters given in DNSConfig will be merged with the policy selected with \
        DNSPolicy. To have DNS options set along with hostNetwork, you have to specify \
        DNS policy explicitly to 'ClusterFirstWithHostNet'.
    :type dns_policy: Optional[str]
    :param enable_service_links:EnableServiceLinks indicates whether information about \
        services should be injected into pod's environment variables, matching the \
        syntax of Docker links. Optional: Defaults to true.
    :type enable_service_links: Optional[bool]
    :param ephemeral_containers:List of ephemeral containers run in this pod. \
        Ephemeral containers may be run in an existing pod to perform user-initiated \
        actions such as debugging. This list cannot be specified when creating a pod, \
        and it cannot be modified by updating the pod spec. In order to add an \
        ephemeral container to an existing pod, use the pod's ephemeralcontainers \
        subresource. This field is alpha-level and is only honored by servers that \
        enable the EphemeralContainers feature.
    :type ephemeral_containers: Optional[List[EphemeralContainer]]
    :param host_aliases:HostAliases is an optional list of hosts and IPs that will be \
        injected into the pod's hosts file if specified. This is only valid for \
        non-hostNetwork pods.
    :type host_aliases: Optional[List[HostAlias]]
    :param host_ipc:Use the host's ipc namespace. Optional: Default to false.
    :type host_ipc: Optional[bool]
    :param host_network:Host networking requested for this pod. Use the host's network \
        namespace. If this option is set, the ports that will be used must be \
        specified. Default to false.
    :type host_network: Optional[bool]
    :param host_pid:Use the host's pid namespace. Optional: Default to false.
    :type host_pid: Optional[bool]
    :param hostname:Specifies the hostname of the Pod If not specified, the pod's \
        hostname will be set to a system-defined value.
    :type hostname: Optional[str]
    :param image_pull_secrets:ImagePullSecrets is an optional list of references to \
        secrets in the same namespace to use for pulling any of the images used by \
        this PodSpec. If specified, these secrets will be passed to individual puller \
        implementations for them to use. For example, in the case of docker, only \
        DockerConfig type secrets are honored. More info: \
        https://kubernetes.io/docs/concepts/containers/images#specifying-imagepullsecrets-on-a-pod  # noqa
    :type image_pull_secrets: Optional[List[LocalObjectReference]]
    :param init_containers:List of initialization containers belonging to the pod. \
        Init containers are executed in order prior to containers being started. If \
        any init container fails, the pod is considered to have failed and is handled \
        according to its restartPolicy. The name for an init container or normal \
        container must be unique among all containers. Init containers may not have \
        Lifecycle actions, Readiness probes, Liveness probes, or Startup probes. The \
        resourceRequirements of an init container are taken into account during \
        scheduling by finding the highest request/limit for each resource type, and \
        then using the max of of that value or the sum of the normal containers. \
        Limits are applied to init containers in a similar fashion. Init containers \
        cannot currently be added or removed. Cannot be updated. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
    :type init_containers: Optional[List[Container]]
    :param node_name:NodeName is a request to schedule this pod onto a specific node. \
        If it is non-empty, the scheduler simply schedules this pod onto that node, \
        assuming that it fits resource requirements.
    :type node_name: Optional[str]
    :param node_selector:NodeSelector is a selector which must be true for the pod to \
        fit on a node. Selector which must match a node's labels for the pod to be \
        scheduled on that node. More info: \
        https://kubernetes.io/docs/concepts/configuration/assign-pod-node/
    :type node_selector: Optional[dict]
    :param overhead:Overhead represents the resource overhead associated with running \
        a pod for a given RuntimeClass. This field will be autopopulated at admission \
        time by the RuntimeClass admission controller. If the RuntimeClass admission \
        controller is enabled, overhead must not be set in Pod create requests. The \
        RuntimeClass admission controller will reject Pod create requests which have \
        the overhead already set. If RuntimeClass is configured and selected in the \
        PodSpec, Overhead will be set to the value defined in the corresponding \
        RuntimeClass, otherwise it will remain unset and treated as zero. More info: \
        https://git.k8s.io/enhancements/keps/sig-node/20190226-pod-overhead.md This \
        field is alpha-level as of Kubernetes v1.16, and is only honored by servers \
        that enable the PodOverhead feature.
    :type overhead: Optional[dict]
    :param preemption_policy:PreemptionPolicy is the Policy for preempting pods with \
        lower priority. One of Never, PreemptLowerPriority. Defaults to \
        PreemptLowerPriority if unset. This field is alpha-level and is only honored \
        by servers that enable the NonPreemptingPriority feature.
    :type preemption_policy: Optional[str]
    :param priority:The priority value. Various system components use this field to \
        find the priority of the pod. When Priority Admission Controller is enabled, \
        it prevents users from setting this field. The admission controller populates \
        this field from PriorityClassName. The higher the value, the higher the \
        priority.
    :type priority: Optional[int]
    :param priority_class_name:If specified, indicates the pod's priority. \
        "system-node-critical" and "system-cluster-critical" are two special keywords \
        which indicate the highest priorities with the former being the highest \
        priority. Any other name must be defined by creating a PriorityClass object \
        with that name. If not specified, the pod priority will be default or zero if \
        there is no default.
    :type priority_class_name: Optional[str]
    :param readiness_gates:If specified, all readiness gates will be evaluated for pod \
        readiness. A pod is ready when all its containers are ready AND all conditions \
        specified in the readiness gates have status equal to "True" More info: \
        https://git.k8s.io/enhancements/keps/sig-network/0007-pod-ready%2B%2B.md
    :type readiness_gates: Optional[List[PodReadinessGate]]
    :param restart_policy:Restart policy for all containers within the pod. One of \
        Always, OnFailure, Never. Default to Always. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy  # noqa
    :type restart_policy: Optional[str]
    :param runtime_class_name:RuntimeClassName refers to a RuntimeClass object in the \
        node.k8s.io group, which should be used to run this pod.  If no RuntimeClass \
        resource matches the named class, the pod will not be run. If unset or empty, \
        the "legacy" RuntimeClass will be used, which is an implicit class with an \
        empty definition that uses the default runtime handler. More info: \
        https://git.k8s.io/enhancements/keps/sig-node/runtime-class.md This is a beta \
        feature as of Kubernetes v1.14.
    :type runtime_class_name: Optional[str]
    :param scheduler_name:If specified, the pod will be dispatched by specified \
        scheduler. If not specified, the pod will be dispatched by default scheduler.
    :type scheduler_name: Optional[str]
    :param security_context:SecurityContext holds pod-level security attributes and \
        common container settings. Optional: Defaults to empty.  See type description \
        for default values of each field.
    :type security_context: Optional[PodSecurityContext]
    :param service_account:DeprecatedServiceAccount is a depreciated alias for \
        ServiceAccountName. Deprecated: Use serviceAccountName instead.
    :type service_account: Optional[str]
    :param service_account_name:ServiceAccountName is the name of the ServiceAccount \
        to use to run this pod. More info: \
        https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/  # noqa
    :type service_account_name: Optional[str]
    :param share_process_namespace:Share a single process namespace between all of the \
        containers in a pod. When this is set containers will be able to view and \
        signal processes from other containers in the same pod, and the first process \
        in each container will not be assigned PID 1. HostPID and \
        ShareProcessNamespace cannot both be set. Optional: Default to false.
    :type share_process_namespace: Optional[bool]
    :param subdomain:If specified, the fully qualified Pod hostname will be \
        "<hostname>.<subdomain>.<pod namespace>.svc.<cluster domain>". If not \
        specified, the pod will not have a domainname at all.
    :type subdomain: Optional[str]
    :param termination_grace_period_seconds:Optional duration in seconds the pod needs \
        to terminate gracefully. May be decreased in delete request. Value must be \
        non-negative integer. The value zero indicates delete immediately. If this \
        value is nil, the default grace period will be used instead. The grace period \
        is the duration in seconds after the processes running in the pod are sent a \
        termination signal and the time when the processes are forcibly halted with a \
        kill signal. Set this value longer than the expected cleanup time for your \
        process. Defaults to 30 seconds.
    :type termination_grace_period_seconds: Optional[int]
    :param tolerations:If specified, the pod's tolerations.
    :type tolerations: Optional[List[Toleration]]
    :param topology_spread_constraints:TopologySpreadConstraints describes how a group \
        of pods ought to spread across topology domains. Scheduler will schedule pods \
        in a way which abides by the constraints. This field is only honored by \
        clusters that enable the EvenPodsSpread feature. All topologySpreadConstraints \
        are ANDed.
    :type topology_spread_constraints: Optional[List[TopologySpreadConstraint]]
    :param volumes:List of volumes that can be mounted by containers belonging to the \
        pod. More info: https://kubernetes.io/docs/concepts/storage/volumes
    :type volumes: Optional[List[Volume]]
    """

    def __init__(
        self,
        containers: List[Container],
        active_deadline_seconds: Optional[int] = None,
        affinity: Optional[Affinity] = None,
        automount_service_account_token: Optional[bool] = None,
        dns_config: Optional[PodDNSConfig] = None,
        dns_policy: Optional[str] = None,
        enable_service_links: Optional[bool] = None,
        ephemeral_containers: Optional[List[EphemeralContainer]] = None,
        host_aliases: Optional[List[HostAlias]] = None,
        host_ipc: Optional[bool] = None,
        host_network: Optional[bool] = None,
        host_pid: Optional[bool] = None,
        hostname: Optional[str] = None,
        image_pull_secrets: Optional[List[LocalObjectReference]] = None,
        init_containers: Optional[List[Container]] = None,
        node_name: Optional[str] = None,
        node_selector: Optional[dict] = None,
        overhead: Optional[dict] = None,
        preemption_policy: Optional[str] = None,
        priority: Optional[int] = None,
        priority_class_name: Optional[str] = None,
        readiness_gates: Optional[List[PodReadinessGate]] = None,
        restart_policy: Optional[str] = None,
        runtime_class_name: Optional[str] = None,
        scheduler_name: Optional[str] = None,
        security_context: Optional[PodSecurityContext] = None,
        service_account: Optional[str] = None,
        service_account_name: Optional[str] = None,
        share_process_namespace: Optional[bool] = None,
        subdomain: Optional[str] = None,
        termination_grace_period_seconds: Optional[int] = None,
        tolerations: Optional[List[Toleration]] = None,
        topology_spread_constraints: Optional[List[TopologySpreadConstraint]] = None,
        volumes: Optional[List[Volume]] = None,
    ):
        self.containers = containers
        self.activeDeadlineSeconds = active_deadline_seconds
        self.affinity = affinity
        self.automountServiceAccountToken = automount_service_account_token
        self.dnsConfig = dns_config
        self.dnsPolicy = dns_policy
        self.enableServiceLinks = enable_service_links
        self.ephemeralContainers = ephemeral_containers
        self.hostAliases = host_aliases
        self.hostIPC = host_ipc
        self.hostNetwork = host_network
        self.hostPID = host_pid
        self.hostname = hostname
        self.imagePullSecrets = image_pull_secrets
        self.initContainers = init_containers
        self.nodeName = node_name
        self.nodeSelector = node_selector
        self.overhead = overhead
        self.preemptionPolicy = preemption_policy
        self.priority = priority
        self.priorityClassName = priority_class_name
        self.readinessGates = readiness_gates
        self.restartPolicy = restart_policy
        self.runtimeClassName = runtime_class_name
        self.schedulerName = scheduler_name
        self.securityContext = security_context
        self.serviceAccount = service_account
        self.serviceAccountName = service_account_name
        self.shareProcessNamespace = share_process_namespace
        self.subdomain = subdomain
        self.terminationGracePeriodSeconds = termination_grace_period_seconds
        self.tolerations = tolerations
        self.topologySpreadConstraints = topology_spread_constraints
        self.volumes = volumes


class PodTemplateSpec(HelmYaml):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the desired behavior of the pod. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: PodSpec
    """

    def __init__(self, metadata: ObjectMeta, spec: PodSpec):
        self.metadata = metadata
        self.spec = spec


class ClientIPConfig(HelmYaml):
    """
    :param timeout_seconds:timeoutSeconds specifies the seconds of ClientIP type \
        session sticky time. The value must be >0 && <=86400(for 1 day) if \
        ServiceAffinity == "ClientIP". Default value is 10800(for 3 hours).
    :type timeout_seconds: int
    """

    def __init__(self, timeout_seconds: int):
        self.timeoutSeconds = timeout_seconds


class SessionAffinityConfig(HelmYaml):
    """
    :param client_ip:clientIP contains the configurations of Client IP based session \
        affinity.
    :type client_ip: ClientIPConfig
    """

    def __init__(self, client_ip: ClientIPConfig):
        self.clientIP = client_ip


class PodIP(HelmYaml):
    """
    :param ip:ip is an IP address (IPv4 or IPv6) assigned to the pod
    :type ip: str
    """

    def __init__(self, ip: str):
        self.ip = ip


class PodCondition(HelmYaml):
    """
    :param last_probe_time:Last time we probed the condition.
    :type last_probe_time: time
    :param last_transition_time:Last time the condition transitioned from one status \
        to another.
    :type last_transition_time: time
    :param message:Human-readable message indicating details about last transition.
    :type message: str
    :param reason:Unique, one-word, CamelCase reason for the condition's last \
        transition.
    :type reason: str
    :param type:Type is the type of the condition. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#pod-conditions  # noqa
    :type type: str
    """

    def __init__(
        self,
        last_probe_time: time,
        last_transition_time: time,
        message: str,
        reason: str,
        type: str,
    ):
        self.lastProbeTime = last_probe_time
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class Pod(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the desired behavior of the pod. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: PodSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: PodSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class PodList(KubernetesBaseObject):
    """
    :param items:List of pods. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md  # noqa
    :type items: List[Pod]
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
        self, items: List[Pod], metadata: ListMeta, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class PodTemplate(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param template:Template defines the pods that will be created from this pod \
        template. \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type template: PodTemplateSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        template: PodTemplateSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.template = template


class PodTemplateList(KubernetesBaseObject):
    """
    :param items:List of pod templates
    :type items: List[PodTemplate]
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
        items: List[PodTemplate],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
