import pytest

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.metadata import ObjectMeta
from helm_factory.kubernetes_objects.deployment import DeploymentSpec, Deployment
from helm_factory.kubernetes_objects.pod import PodSpec, PodTemplateSpec
from helm_factory.kubernetes_objects.container import Container


@pytest.fixture
def metadata():
    return ObjectMeta(annotations={"role": "user"},)


@pytest.mark.parametrize(
    "args,yaml",
    [
        (
            {
                "api_version": "v1",
                "kind": "Deployment",
                "metadata": ObjectMeta(name="test"),
            },
            """apiVersion: v1
kind: Deployment
metadata:
  name: test
""",
        ),
        (
            {
                "api_version": "v1",
                "kind": "Deployment",
                "metadata": ObjectMeta(
                    name="test",
                    annotations={"role": "user", "type": "worker"},
                    labels={"role": "user", "type": "worker"},
                    namespace="default",
                ),
            },
            """apiVersion: v1
kind: Deployment
metadata:
  annotations:
    role: user
    type: worker
  labels:
    role: user
    type: worker
  name: test
  namespace: default
""",
        ),
        (
            {
                "api_version": "v1",
                "kind": "Deployment",
                "metadata": ObjectMeta(
                    name="test",
                    labels=None,
                    namespace="default",
                    annotations={"role": "user", "type": "worker"},
                ),
            },
            """apiVersion: v1
kind: Deployment
metadata:
  annotations:
    role: user
    type: worker
  name: test
  namespace: default
""",
        ),
    ],
)
def test_kube_base_object(args: dict, yaml: str):
    base_object = KubernetesBaseObject(**args)
    assert str(base_object) == yaml

def test_create_deployment():
    deployment = Deployment(
        api_version="v1",
        metadata=ObjectMeta(name="test_deployment", labels={"type": "master"}),
        spec=DeploymentSpec(
            replicas=1,
            template=PodTemplateSpec(
                ObjectMeta(labels={"container_type": "master"}),
                spec=PodSpec(containers=[Container(image="test-image")]),
            ),
        ),
    )
    assert (
        str(deployment)
        == """apiVersion: v1
kind: Deployment
metadata:
  labels:
    type: master
  name: test_deployment
spec:
  replicas: 1
  template:
    metadata:
      labels:
        container_type: master
    spec:
      containers:
      - image: test-image
"""
    )