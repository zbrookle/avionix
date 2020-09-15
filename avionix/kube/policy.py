"""
Contains various policy based classes
"""

from typing import List, Optional, Union

from avionix.kube.base_objects import Policy
from avionix.kube.core import SELinuxOptions
from avionix.kube.meta import DeleteOptions, LabelSelector, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class IDRange(HelmYaml):
    """
    :param min: min is the start of the range, inclusive.
    :param max: max is the end of the range, inclusive.
    """

    def __init__(self, min: int, max: int):
        self.max = max
        self.min = min


class SupplementalGroupsStrategyOptions(HelmYaml):
    """
    :param rule: rule is the strategy that will dictate what supplemental groups is \
        used in the SecurityContext.
    :param ranges: ranges are the allowed ranges of supplemental groups.  If you would \
        like to force a single supplemental group then supply a single range with the \
        same start and end. Required for MustRunAs.
    """

    def __init__(self, rule: str, ranges: Optional[List[IDRange]] = None):
        self.ranges = ranges
        self.rule = rule


class RuntimeClassStrategyOptions(HelmYaml):
    """
    :param allowed_runtime_class_names: allowedRuntimeClassNames is a whitelist of \
        RuntimeClass names that may be specified on a pod. A value of "*" means that \
        any RuntimeClass name is allowed, and must be the only item in the list. An \
        empty list requires the RuntimeClassName field to be unset.
    :param default_runtime_class_name: defaultRuntimeClassName is the default \
        RuntimeClassName to set on the pod. The default MUST be allowed by the \
        allowedRuntimeClassNames list. A value of nil does not mutate the Pod.
    """

    def __init__(
        self,
        allowed_runtime_class_names: List[str],
        default_runtime_class_name: Optional[str] = None,
    ):
        self.allowedRuntimeClassNames = allowed_runtime_class_names
        self.defaultRuntimeClassName = default_runtime_class_name


class PodDisruptionBudgetSpec(HelmYaml):
    """
    :param max_unavailable: An eviction is allowed if at most "maxUnavailable" pods \
        selected by "selector" are unavailable after the eviction, i.e. even in \
        absence of the evicted pod. For example, one can prevent all voluntary \
        evictions by specifying 0. This is a mutually exclusive setting with \
        "minAvailable".
    :param min_available: An eviction is allowed if at least "minAvailable" pods \
        selected by "selector" will still be available after the eviction, i.e. even \
        in the absence of the evicted pod.  So for example you can prevent all \
        voluntary evictions by specifying "100%".
    :param selector: Label query over pods whose evictions are managed by the \
        disruption budget.
    """

    def __init__(
        self,
        max_unavailable: Optional[Union[int, str]] = None,
        min_available: Optional[Union[int, str]] = None,
        selector: Optional[LabelSelector] = None,
    ):
        self.maxUnavailable = max_unavailable
        self.minAvailable = min_available
        self.selector = selector


class PodDisruptionBudget(Policy):
    """
    :param metadata: None
    :param spec: Specification of the desired behavior of the PodDisruptionBudget.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    _non_standard_version = "v1beta1"

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: PodDisruptionBudgetSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class Eviction(Policy):
    """
    :param metadata: ObjectMeta describes the pod that is being evicted.
    :param delete_options: DeleteOptions may be provided
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    _non_standard_version = "v1beta1"

    def __init__(
        self,
        metadata: ObjectMeta,
        delete_options: DeleteOptions,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.deleteOptions = delete_options


class HostPortRange(HelmYaml):
    """
    :param max: max is the end of the range, inclusive.
    :param min: min is the start of the range, inclusive.
    """

    def __init__(self, max: int, min: int):
        self.max = max
        self.min = min


class AllowedHostPath(HelmYaml):
    """
    :param path_prefix: pathPrefix is the path prefix that the host volume must match. \
        It does not support `*`. Trailing slashes are trimmed when validating the path \
        prefix with a host path.  Examples: `/foo` would allow `/foo`, `/foo/` and \
        `/foo/bar` `/foo` would not allow `/food` or `/etc/foo`
    :param read_only: when set to true, will allow host volumes matching the pathPrefix \
        only if all volume mounts are readOnly.
    """

    def __init__(self, path_prefix: str, read_only: Optional[bool] = None):
        self.pathPrefix = path_prefix
        self.readOnly = read_only


class RunAsUserStrategyOptions(HelmYaml):
    """
    :param rule: rule is the strategy that will dictate the allowable RunAsUser values \
        that may be set.
    :param ranges: ranges are the allowed ranges of uids that may be used. If you would \
        like to force a single uid then supply a single range with the same start and \
        end. Required for MustRunAs.
    """

    def __init__(self, rule: str, ranges: Optional[List[IDRange]] = None):
        self.ranges = ranges
        self.rule = rule


class AllowedCSIDriver(HelmYaml):
    """
    :param name: Name is the registered name of the CSI driver
    """

    def __init__(self, name: str):
        self.name = name


class SELinuxStrategyOptions(HelmYaml):
    """
    :param rule: rule is the strategy that will dictate the allowable labels that may \
        be set.
    :param se_linux_options: seLinuxOptions required to run as; required for MustRunAs \
        More info: \
        https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
    """

    def __init__(self, rule: str, se_linux_options: Optional[SELinuxOptions] = None):
        self.rule = rule
        self.seLinuxOptions = se_linux_options


class AllowedFlexVolume(HelmYaml):
    """
    :param driver: driver is the name of the Flexvolume driver.
    """

    def __init__(self, driver: str):
        self.driver = driver


class FSGroupStrategyOptions(HelmYaml):
    """
    :param rule: rule is the strategy that will dictate what FSGroup is used in the \
        SecurityContext.
    :param ranges: ranges are the allowed ranges of fs groups.  If you would like to \
        force a single fs group then supply a single range with the same start and \
        end. Required for MustRunAs.
    """

    def __init__(self, rule: str, ranges: Optional[List[IDRange]] = None):
        self.ranges = ranges
        self.rule = rule


class RunAsGroupStrategyOptions(HelmYaml):
    """
    :param rule: rule is the strategy that will dictate the allowable RunAsGroup values \
        that may be set.
    :param ranges: ranges are the allowed ranges of gids that may be used. If you would \
        like to force a single gid then supply a single range with the same start and \
        end. Required for MustRunAs.
    """

    def __init__(self, rule: str, ranges: Optional[List[IDRange]] = None):
        self.ranges = ranges
        self.rule = rule


class PodSecurityPolicySpec(HelmYaml):
    """
    :param fs_group: fsGroup is the strategy that will dictate what fs group is used by \
        the SecurityContext.
    :param run_as_user: runAsUser is the strategy that will dictate the allowable \
        RunAsUser values that may be set.
    :param se_linux: seLinux is the strategy that will dictate the allowable labels \
        that may be set.
    :param allowed_csidrivers: AllowedCSIDrivers is a whitelist of inline CSI drivers \
        that must be explicitly set to be embedded within a pod spec. An empty value \
        indicates that any CSI driver can be used for inline ephemeral volumes. This \
        is an alpha field, and is only honored if the API server enables the \
        CSIInlineVolume feature gate.
    :param allowed_capabilities: allowedCapabilities is a list of capabilities that can \
        be requested to add to the container. Capabilities in this field may be added \
        at the pod author's discretion. You must not list a capability in both \
        allowedCapabilities and requiredDropCapabilities.
    :param allowed_flex_volumes: allowedFlexVolumes is a whitelist of allowed \
        Flexvolumes.  Empty or nil indicates that all Flexvolumes may be used.  This \
        parameter is effective only when the usage of the Flexvolumes is allowed in \
        the "volumes" field.
    :param allowed_host_paths: allowedHostPaths is a white list of allowed host paths. \
        Empty indicates that all host paths may be used.
    :param allowed_proc_mount_types: AllowedProcMountTypes is a whitelist of allowed \
        ProcMountTypes. Empty or nil indicates that only the DefaultProcMountType may \
        be used. This requires the ProcMountType feature flag to be enabled.
    :param default_add_capabilities: defaultAddCapabilities is the default set of \
        capabilities that will be added to the container unless the pod spec \
        specifically drops the capability.  You may not list a capability in both \
        defaultAddCapabilities and requiredDropCapabilities. Capabilities added here \
        are implicitly allowed, and need not be included in the allowedCapabilities \
        list.
    :param default_allow_privilege_escalation: defaultAllowPrivilegeEscalation controls \
        the default setting for whether a process can gain more privileges than its \
        parent process.
    :param host_ipc: hostIPC determines if the policy allows the use of HostIPC in the \
        pod spec.
    :param host_pid: hostPID determines if the policy allows the use of HostPID in the \
        pod spec.
    :param host_ports: hostPorts determines which host port ranges are allowed to be \
        exposed.
    :param privileged: privileged determines if a pod can request to be run as \
        privileged.
    :param read_only_root_filesystem: readOnlyRootFilesystem when set to true will \
        force containers to run with a read only root file system.  If the container \
        specifically requests to run with a non-read only root file system the PSP \
        should deny the pod. If set to false the container may run with a read only \
        root file system if it wishes but it will not be forced to.
    :param required_drop_capabilities: requiredDropCapabilities are the capabilities \
        that will be dropped from the container.  These are required to be dropped and \
        cannot be added.
    :param run_as_group: RunAsGroup is the strategy that will dictate the allowable \
        RunAsGroup values that may be set. If this field is omitted, the pod's \
        RunAsGroup can take any value. This field requires the RunAsGroup feature gate \
        to be enabled.
    :param runtime_class: runtimeClass is the strategy that will dictate the allowable \
        RuntimeClasses for a pod. If this field is omitted, the pod's runtimeClassName \
        field is unrestricted. Enforcement of this field depends on the RuntimeClass \
        feature gate being enabled.
    :param supplemental_groups: supplementalGroups is the strategy that will dictate \
        what supplemental groups are used by the SecurityContext.
    :param allow_privilege_escalation: allowPrivilegeEscalation determines if a pod can \
        request to allow privilege escalation. If unspecified, defaults to true.
    :param allowed_unsafe_sysctls: allowedUnsafeSysctls is a list of explicitly allowed \
        unsafe sysctls, defaults to none. Each entry is either a plain sysctl name or \
        ends in "*" in which case it is considered as a prefix of allowed sysctls. \
        Single * means all unsafe sysctls are allowed. Kubelet has to whitelist all \
        allowed unsafe sysctls explicitly to avoid rejection.  Examples: e.g. "foo/*" \
        allows "foo/bar", "foo/baz", etc. e.g. "foo.*" allows "foo.bar", "foo.baz", \
        etc.
    :param forbidden_sysctls: forbiddenSysctls is a list of explicitly forbidden \
        sysctls, defaults to none. Each entry is either a plain sysctl name or ends in \
        "*" in which case it is considered as a prefix of forbidden sysctls. Single * \
        means all sysctls are forbidden.  Examples: e.g. "foo/*" forbids "foo/bar", \
        "foo/baz", etc. e.g. "foo.*" forbids "foo.bar", "foo.baz", etc.
    :param host_network: hostNetwork determines if the policy allows the use of \
        HostNetwork in the pod spec.
    :param volumes: volumes is a white list of allowed volume plugins. Empty indicates \
        that no volumes may be used. To allow all volumes you may use '\\*'.
    """

    def __init__(
        self,
        fs_group: FSGroupStrategyOptions,
        run_as_user: RunAsUserStrategyOptions,
        se_linux: SELinuxStrategyOptions,
        supplemental_groups: SupplementalGroupsStrategyOptions,
        allowed_csidrivers: Optional[List[AllowedCSIDriver]] = None,
        allowed_capabilities: Optional[List[str]] = None,
        allowed_flex_volumes: Optional[List[AllowedFlexVolume]] = None,
        allowed_host_paths: Optional[List[AllowedHostPath]] = None,
        allowed_proc_mount_types: Optional[List[str]] = None,
        default_add_capabilities: Optional[List[str]] = None,
        default_allow_privilege_escalation: Optional[bool] = None,
        host_ipc: Optional[bool] = None,
        host_pid: Optional[bool] = None,
        host_ports: Optional[List[HostPortRange]] = None,
        privileged: Optional[bool] = None,
        read_only_root_filesystem: Optional[bool] = None,
        required_drop_capabilities: Optional[List[str]] = None,
        run_as_group: Optional[RunAsGroupStrategyOptions] = None,
        runtime_class: Optional[RuntimeClassStrategyOptions] = None,
        allow_privilege_escalation: Optional[bool] = None,
        allowed_unsafe_sysctls: Optional[List[str]] = None,
        forbidden_sysctls: Optional[List[str]] = None,
        host_network: Optional[bool] = None,
        volumes: Optional[List[str]] = None,
    ):
        self.allowedCSIDrivers = allowed_csidrivers
        self.allowedCapabilities = allowed_capabilities
        self.allowedFlexVolumes = allowed_flex_volumes
        self.allowedHostPaths = allowed_host_paths
        self.allowedProcMountTypes = allowed_proc_mount_types
        self.defaultAddCapabilities = default_add_capabilities
        self.defaultAllowPrivilegeEscalation = default_allow_privilege_escalation
        self.fsGroup = fs_group
        self.hostIPC = host_ipc
        self.hostPID = host_pid
        self.hostPorts = host_ports
        self.privileged = privileged
        self.readOnlyRootFilesystem = read_only_root_filesystem
        self.requiredDropCapabilities = required_drop_capabilities
        self.runAsGroup = run_as_group
        self.runAsUser = run_as_user
        self.runtimeClass = runtime_class
        self.seLinux = se_linux
        self.supplementalGroups = supplemental_groups
        self.allowPrivilegeEscalation = allow_privilege_escalation
        self.allowedUnsafeSysctls = allowed_unsafe_sysctls
        self.forbiddenSysctls = forbidden_sysctls
        self.hostNetwork = host_network
        self.volumes = volumes


class PodSecurityPolicy(Policy):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: spec defines the policy enforced.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    _non_standard_version = "v1beta1"

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: PodSecurityPolicySpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec
