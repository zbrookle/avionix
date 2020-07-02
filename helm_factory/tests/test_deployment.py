from helm_factory.kubernetes_objects.deployment import Deployment, Label
from helm_factory.kubernetes_objects.pod import PodTemplateSpec


def test_create_deployment():
    deployment = Deployment(
        "v1",
        "test_deployment",
        labels=[Label("type", "master")],
        pod_template_spec=PodTemplateSpec(),
    )
    print(str(deployment))
    assert str(deployment) == ""
