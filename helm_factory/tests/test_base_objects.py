from helm_factory.kubernetes_objects import Annotation, KubernetesBaseObject, Label
import pytest


@pytest.mark.parametrize(
    "args,yaml",
    [
        (
            {"api_version": "v1", "kind": "Deployment", "name": "test"},
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
                "name": "test",
                "labels": [Label("role", "user"), Label("type", "worker")],
                "namespace": "default",
                "annotations": [
                    Annotation("role", "user"),
                    Annotation("type", "worker"),
                ],
            },
            """apiVersion: v1
kind: Deployment
metadata:
  annotations:
  - role: user
  - type: worker
  labels:
  - role: user
  - type: worker
  name: test
  namespace: default
""",
        ),
    ],
)
def test_kube_base_object(args: dict, yaml: str):
    base_object = KubernetesBaseObject(**args)
    assert yaml == str(base_object)
