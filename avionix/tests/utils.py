from avionix.kubernetes_objects.container import Container
from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.kubernetes_objects.metadata import ObjectMeta
from avionix.kubernetes_objects.pod import PodSpec, PodTemplateSpec


def get_test_deployment():
    return Deployment(
        metadata=ObjectMeta(name="test_deployment", labels={"type": "master"}),
        spec=DeploymentSpec(
            replicas=1,
            template=PodTemplateSpec(
                ObjectMeta(labels={"container_type": "master"}),
                spec=PodSpec(containers=[Container(image="test-image")]),
            ),
        ),
    )
