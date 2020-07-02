from kubernetes import client, config
import pytest


@pytest.fixture(scope="module")
def load_kubeconfig():
    config.load_kube_config()


@pytest.fixture(scope="module")
def kube_client():
    return client.CoreV1Api()
