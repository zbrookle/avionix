from typing import Optional

from avionix.kube.apps import Deployment, DeploymentSpec
from avionix.kube.core import (
    Container,
    ContainerPort,
    EnvVar,
    Pod,
    PodSecurityContext,
    PodSpec,
    PodTemplateSpec,
    Probe,
    Volume,
    VolumeMount,
)
from avionix.kube.meta import LabelSelector, ObjectMeta
from avionix.testing.helpers import kubectl_get


def get_test_container(number: int):
    return Container(
        name=f"test-container-{number}",
        image="k8s.gcr.io/echoserver:1.4",
        env=[EnvVar("test", "test-value")],
        ports=[ContainerPort(8080)],
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
    info = kubectl_get("events")
    return info[(info["TYPE"] != "Normal") & (info["TYPE"] != "Warning")].reset_index(
        drop=True
    )


def get_pod_with_options(
    volume: Optional[Volume] = None,
    security_context: Optional[PodSecurityContext] = None,
    readiness_probe: Optional[Probe] = None,
):
    container = get_test_container(0)
    if volume is not None:
        container.volumeMounts = [VolumeMount(volume.name, "~/tmp")]
    if readiness_probe is not None:
        container.readinessProbe = readiness_probe
        container.livenessProbe = readiness_probe
        container.startupProbe = readiness_probe
    return Pod(
        ObjectMeta(name="test-pod"),
        PodSpec([container], volumes=[volume], security_context=security_context),
    )
