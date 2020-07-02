from helm_factory.kubernetes_objects.container import Container
from helm_factory.kubernetes_objects.volumes import Volume
from helm_factory.kubernetes_objects.shared_objects import Toleration
from helm_factory.kubernetes_objects.base_objects import BaseSpec
from typing import List, Optional


class Affinity:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#affinity-v1-core
    """

    pass


class PodDnsConfig:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#poddnsconfig-v1-core
    """

    pass


class PodSecurityContext:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#podsecuritycontext-v1-core
    """


class HostAlias:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#hostalias-v1-core
    """

    def __init__(self, hostnames: List[str], ip: str):
        self.hostnames = hostnames
        self.ip = ip


class TopologySpreadConstraint:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#topologyspreadconstraint-v1-core
    """


class EphemeralContainer:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#ephemeralcontainer-v1-core
    """

    pass


class PodTemplateSpec(BaseSpec):
    def __init__(
        self,
        automount_service_account_token: bool,
        containers: List[Container],
        active_deadline_seconds: Optional[int] = None,
        affinity: Optional[Affinity] = None,
        dns_config: Optional[PodDnsConfig] = None,
        dns_policy: Optional[str] = None,
        enable_service_links: Optional[bool] = None,
        ephemeral_containers: Optional[List[Container]] = None,
        share_process_namespace: Optional[bool] = None,
        host_aliases: Optional[List[HostAlias]] = None,
        host_ipc: Optional[bool] = None,
        host_network: Optional[bool] = None,
        host_pid: Optional[bool] = None,
        hostname: Optional[str] = None,
        image_pull_secrets: Optional[List[str]] = None,
        init_containers: Optional[List[Container]] = None,
        node_name: Optional[str] = None,
        node_selector=None,
        overhead=None,
        termination_grace_period_seconds: Optional[int] = None,
        preemption_policy: str = None,
        priority: Optional[int] = None,
        priority_class_name: Optional[str] = None,
        readiness_condition_types: List[str] = None,
        restart_policy: Optional[str] = None,
        runtime_class_name: Optional[str] = None,
        scheduler_name: Optional[str] = None,
        security_context: Optional[PodSecurityContext] = None,
        service_account_name: Optional[str] = None,
        subdomain: Optional[str] = None,
        tolerations: List[Toleration] = None,
        topology_spread_constraints: List[TopologySpreadConstraint] = None,
        volumes: List[Volume] = None,
    ):
        assert containers, "Must give at least one container for a pod"
        self.activeDeadlineSeconds = active_deadline_seconds
        self.affinity = affinity
        self.automountServiceAccountToken = automount_service_account_token
        self.dnsConfig = dns_config
        self.dnsPolicy = dns_policy
        self.enableServiceLinks = enable_service_links
        self.ephemeralContainers = ephemeral_containers
        self.shareProcessNamespace = share_process_namespace
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
        self.terminationGracePeriodSeconds = termination_grace_period_seconds
        self.preemptionPolicy = preemption_policy
        self.priority = priority
        self.priorityClassName = priority_class_name
        self.readiness_condition_types = readiness_condition_types
        self.restartPolicy = restart_policy
        self.runtimeClassName = runtime_class_name
        self.schedulerName = scheduler_name
        self.securityContext = security_context
        self.serviceAccountName = service_account_name
        self.subdomain = subdomain
        self.tolerations = tolerations
        self.topologySpreadConstraints = topology_spread_constraints
        self.volumes = volumes
