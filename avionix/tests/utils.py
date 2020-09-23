from typing import List, Optional

from pandas import DataFrame

from avionix.kube.apps import Deployment, DeploymentSpec
from avionix.kube.core import (
    Affinity,
    Container,
    ContainerPort,
    EnvFromSource,
    EnvVar,
    EphemeralContainer,
    HostAlias,
    Lifecycle,
    Pod,
    PodDNSConfig,
    PodSecurityContext,
    PodSpec,
    PodTemplateSpec,
    Probe,
    SecurityContext,
    TopologySpreadConstraint,
    Volume,
    VolumeDevice,
    VolumeMount,
)
from avionix.kube.meta import LabelSelector, ObjectMeta
from avionix.testing.helpers import kubectl_get


def get_test_container(
    number: int, env_var: Optional[EnvVar] = None, ephemeral: bool = False
):
    container_class = Container
    if ephemeral:
        container_class = EphemeralContainer
    if env_var is None:
        env_var = EnvVar("test", "test-value")
    return container_class(
        name=f"test-container-{number}",
        image="k8s.gcr.io/echoserver:1.4",
        env=[env_var],
        ports=[ContainerPort(8080, name="port")],
    )


def get_test_deployment(number: int):
    return Deployment(
        metadata=ObjectMeta(
            name=f"test-deployment-{number}", labels={"type": "master"}
        ),
        spec=DeploymentSpec(
            replicas=1,
            template=PodTemplateSpec(
                ObjectMeta(labels={"container_type": "master"}),
                spec=PodSpec(containers=[get_test_container(number)]),
            ),
            selector=LabelSelector(match_labels={"container_type": "master"}),
        ),
    )


def get_event_info():
    info = DataFrame(kubectl_get("events"))
    return info[(info["TYPE"] != "Normal") & (info["TYPE"] != "Warning")].reset_index(
        drop=True
    )


def get_pod_with_options(
    volume: Optional[Volume] = None,
    volume_mount: Optional[VolumeMount] = None,
    pod_security_context: Optional[PodSecurityContext] = None,
    readiness_probe: Optional[Probe] = None,
    environment_var: Optional[EnvVar] = None,
    volume_device: Optional[VolumeDevice] = None,
    command: Optional[List[str]] = None,
    container_security_context: Optional[SecurityContext] = None,
    lifecycle: Optional[Lifecycle] = None,
    host_alias: Optional[HostAlias] = None,
    env_from: Optional[List[EnvFromSource]] = None,
    topology_spread: Optional[TopologySpreadConstraint] = None,
    dns_config: Optional[PodDNSConfig] = None,
    ephemeral: bool = False,
    affinity: Optional[Affinity] = None,
    name: str = "test-pod",
):
    container = get_test_container(0, environment_var, ephemeral)
    if volume_mount is not None:
        container.volumeMounts = [volume_mount]
    if volume_device is not None:
        container.volumeDevices = [volume_device]
    if readiness_probe is not None:
        container.readinessProbe = readiness_probe
        container.livenessProbe = readiness_probe
        container.startupProbe = readiness_probe
    container.securityContext = container_security_context
    container.command = command
    container.lifecycle = lifecycle
    container.envFrom = env_from
    return Pod(
        ObjectMeta(name=name),
        PodSpec(
            [container],
            volumes=[volume],
            security_context=pod_security_context,
            host_aliases=[host_alias],
            topology_spread_constraints=[topology_spread],
            dns_config=dns_config,
            affinity=affinity,
        ),
    )
