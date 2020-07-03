from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import BaseSpec, HelmYaml
from helm_factory.kubernetes_objects.key_values_pairs import Label
from helm_factory.kubernetes_objects.shared_objects import Toleration
from helm_factory.kubernetes_objects.volumes import Volume


class Affinity:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#affinity-v1-core
    """


class EnvVar:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#envvar-v1-core
    """


class EnvFromSource:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#envfromsource-v1-core
    """


class LifeCycle:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#lifecycle-v1-core
    """


class Probe:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#probe-v1-core
    """


class ContainerPort:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#containerport-v1-core
    """


class VolumeMount:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#volumemount-v1-core
    """


class VolumeDevice:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#volumedevice-v1-core
    """


class Container(HelmYaml):
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#container-v1-core
    """

    def __init__(
        self,
        args: Optional[List[str]] = None,
        command: Optional[List[str]] = None,
        env: Optional[List[EnvVar]] = None,
        env_from: Optional[List[EnvFromSource]] = None,
        image: Optional[str] = None,
        image_pull_policy: Optional[str] = None,
        lifecycle: Optional[LifeCycle] = None,
        liveness_probe: Optional[Probe] = None,
        name: Optional[str] = None,
        ports: Optional[List[ContainerPort]] = None,
        readiness_probe: Optional[List[Probe]] = None,
        stdin: Optional[bool] = None,
        stdin_once: Optional[bool] = None,
        termination_message_path: Optional[str] = None,
        termination_message_policy: Optional[str] = None,
        tty: Optional[bool] = None,
        volume_devices: Optional[List[VolumeDevice]] = None,
        volume_mounts: Optional[List[VolumeMount]] = None,
        working_dir: Optional[str] = None,
    ):
        self.args = args
        self.command = command
        self.env = env
        self.envFrom = env_from
        self.image = image
        self.imagePullPolicy = image_pull_policy
        self.lifecycle = lifecycle
        self.livenessProbe = liveness_probe
        self.name = name
        self.ports = ports
        self.readinessProbe = readiness_probe
        self.stdin = stdin
        self.stdinOnce = stdin_once
        self.terminationMessagePath = termination_message_path
        self.terminationMessagePolicy = termination_message_policy
        self.tty = tty
        self.volumeDevices = volume_devices
        self.volumeMounts = volume_mounts
        self.workingDir = working_dir


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
        containers: List[Container],
        labels: Optional[List[Label]] = None,
        automount_service_account_token: Optional[bool] = None,
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
        preemption_policy: Optional[str] = None,
        priority: Optional[int] = None,
        priority_class_name: Optional[str] = None,
        readiness_condition_types: Optional[List[str]] = None,
        restart_policy: Optional[str] = None,
        runtime_class_name: Optional[str] = None,
        scheduler_name: Optional[str] = None,
        security_context: Optional[PodSecurityContext] = None,
        service_account_name: Optional[str] = None,
        subdomain: Optional[str] = None,
        tolerations: Optional[List[Toleration]] = None,
        topology_spread_constraints: List[TopologySpreadConstraint] = None,
        volumes: Optional[List[Volume]] = None,
    ):
        assert containers, "Must give at least one container for a pod"
        self.containers = containers
        if labels is None:
            labels = []
        self.metadata = {"labels": [label.get_label_dict() for label in labels]}
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
