from kubernetes import client, config
import pytest
import os
from pathlib import Path
import logging

logging.basicConfig(format="[%(filename)s: %(lineno)s] %(message)s", level=logging.INFO)

KUBE_CONFIG_PATH = Path(__file__).parent / "test_config" / "kubeconfig.yaml"


def get_profile_text():
    return (
        f"""apiVersion: v1
clusters:
- cluster:
    certificate-authority: {Path.home()}/.minikube/ca.crt
    server: https://127.0.0.1:32776
  name: minikube
contexts:
- context:
    cluster: minikube
    user: minikube
  name: minikube
current-context: minikube
kind: Config
"""
        """preferences: {}"""
        f"""
users:
- name: minikube
  user:
    client-certificate: {Path.home()}/.minikube/profiles/minikube/client.crt
    client-key: {Path.home()}/.minikube/profiles/minikube/client.key"""
    )


@pytest.fixture(scope="session", autouse=True)
def set_kubeconfig_env():
    with open(KUBE_CONFIG_PATH, "w") as config_file:
        config_file.write(get_profile_text())
    os.environ["KUBECONFIG"] = str(KUBE_CONFIG_PATH)
    yield
    os.unsetenv("KUBECONFIG")


@pytest.fixture(scope="session")
def load_kubeconfig():
    config.load_kube_config()


@pytest.fixture(scope="session")
def kube_client():
    return client.CoreV1Api()


if __name__ == "__main__":
    print(get_profile_text())
