from helm_factory.kubernetes_objects.deployment import Deployment, Label
from helm_factory.kubernetes_objects.pod import PodTemplateSpec, Container


def test_create_deployment():
    deployment = Deployment(
        "v1",
        "test_deployment",
        labels=[Label("type", "master")],
        pod_template_spec=PodTemplateSpec(
            [Container(image="test_image")], labels=[Label("container_type", "master")],
        ),
    )
    print(str(deployment))
    assert str(deployment) == ""
