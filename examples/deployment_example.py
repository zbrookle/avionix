from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kubernetes_objects.core import (
    PodSpec,
    LabelSelector,
    Container,
    ContainerPort,
    EnvVar,
)
from avionix.kubernetes_objects.apps import Deployment, DeploymentSpec, PodTemplateSpec

container = Container(
    name=f"test-container",
    image="k8s.gcr.io/echoserver:1.4",
    env=[EnvVar("test", "test-value")],
    ports=[ContainerPort(8080)],
)

deployment = Deployment(
    metadata=ObjectMeta(name=f"test-deployment", labels={"app": "my_app"}),
    spec=DeploymentSpec(
        replicas=1,
        template=PodTemplateSpec(
            ObjectMeta(labels={"app": "my_app"}),
            spec=PodSpec(containers=[container]),
        ),
        selector=LabelSelector(match_labels={"app": "my_app"}),
    ),
)

builder = ChartBuilder(
    ChartInfo(api_version="3.2.4", name="test", version="0.1.0", app_version="v1"),
    [deployment],
)