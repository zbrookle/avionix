from helm_factory.kubernetes_objects.deployment import Deployment, Label
from helm_factory.kubernetes_objects.pod import Container, PodTemplateSpec


def test_create_deployment():
    deployment = Deployment(
        "v1",
        "test_deployment",
        labels=[Label("type", "master")],
        pod_template_spec=PodTemplateSpec(
            [Container(image="test_image")], labels=[Label("container_type", "master")],
        ),
    )
    assert (
        str(deployment)
        == """apiVersion: v1
kind: Deployment
metadata:
  labels:
  - type: master
  name: test_deployment
spec:
  replicas: 1
  template:
    spec:
      containers:
      - image: test_image
      metadata:
        labels:
        - container_type: master
"""
    )
