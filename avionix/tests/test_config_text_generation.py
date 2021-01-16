from typing import Optional

import pytest

from avionix.kube.apps import Deployment
from avionix.kube.base_objects import Extensions, KubernetesBaseObject
from avionix.kube.meta import ObjectMeta
from avionix.options import DEFAULTS
from avionix.tests.utils import get_test_deployment


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


def test_create_deployment(test_deployment1: Deployment):
    assert (
        str(test_deployment1)
        == """apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    type: master
  name: test-deployment-1
spec:
  replicas: 1
  selector:
    matchLabels:
      container_type: master
  template:
    metadata:
      labels:
        container_type: master
    spec:
      containers:
      - env:
        - name: test
          value: test-value
        image: k8s.gcr.io/echoserver:1.4
        name: test-container-1
        ports:
        - containerPort: 8080
          name: port
"""
    )


def test_default_version_option():
    preset_default_version = get_test_deployment(1)
    assert preset_default_version.apiVersion == "apps/v1"

    DEFAULTS["default_api_version"] = "v2"
    changed_default_version = get_test_deployment(1)
    assert changed_default_version.apiVersion == "apps/v2"

    # Restore option state
    DEFAULTS["default_api_version"] = "v1"


@pytest.mark.parametrize(
    "version,expected_api_version",
    [(None, "extensions/v1beta1"), ("networking.k8s.io/v1", "networking.k8s.io/v1")],
)
def test_user_version_priority(
    version: str, expected_api_version: str, dependency_chart_info
):
    class NonStandardVersionClass(Extensions):
        _non_standard_version = "v1beta1"

        def __init__(self, metadata: ObjectMeta, api_version: Optional[str] = None):
            super().__init__(api_version)
            self.metadata = metadata

    version_class = NonStandardVersionClass(
        ObjectMeta(name="test"), api_version=version
    )
    assert version_class.apiVersion == expected_api_version
