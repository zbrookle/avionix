import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.apps import (
    ControllerRevision,
    DaemonSet,
    DaemonSetSpec,
    Deployment,
    DeploymentSpec,
    ReplicaSet,
    ReplicaSetSpec,
)
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def controller_revision():
    return ControllerRevision(
        ObjectMeta(name="test-controller-revision"), {"test": "yes"}, 1
    )


def test_controller_revision(chart_info, test_folder, controller_revision):
    builder = ChartBuilder(chart_info, [controller_revision], test_folder)
    with ChartInstallationContext(builder):
        controller_revision_info = kubectl_get("controllerrevisions")
        assert controller_revision_info["NAME"][0] == "test-controller-revision"
        assert controller_revision_info["REVISION"][0] == "1"


@pytest.fixture
def daemon_set(pod_template_spec, selector):
    return DaemonSet(
        ObjectMeta(name="test-daemon-set"), DaemonSetSpec(pod_template_spec, selector),
    )


def test_daemon_set(chart_info, test_folder, daemon_set):
    builder = ChartBuilder(chart_info, [daemon_set], test_folder)
    with ChartInstallationContext(builder):
        daemon_set_info = kubectl_get("daemonsets")
        assert daemon_set_info["NAME"][0] == "test-daemon-set"
        assert daemon_set_info["DESIRED"][0] == "1"
        assert daemon_set_info["CURRENT"][0] == "1"


@pytest.fixture
def deployment(test_labels, pod_template_spec, selector):
    return Deployment(
        metadata=ObjectMeta(name="test-deployment", labels=test_labels),
        spec=DeploymentSpec(replicas=1, template=pod_template_spec, selector=selector,),
    )


def test_deployment(chart_info, test_folder, deployment):
    builder = ChartBuilder(chart_info, [deployment], test_folder)
    with ChartInstallationContext(builder):
        deployment_info = kubectl_get("deployments")
        assert deployment_info["NAME"][0] == "test-deployment"
        assert deployment_info["READY"][0] == "1/1"


@pytest.fixture
def replica_set(pod_template_spec, selector):
    return ReplicaSet(
        ObjectMeta(name="test-replica-set"),
        ReplicaSetSpec(pod_template_spec, selector),
    )


def test_replica_set(chart_info, test_folder, replica_set):
    builder = ChartBuilder(chart_info, [replica_set], test_folder)
    with ChartInstallationContext(builder):
        replica_set_info = kubectl_get("replicasets")
        assert replica_set_info["NAME"][0] == "test-replica-set"
        assert replica_set_info["DESIRED"][0] == "1"
        assert replica_set_info["CURRENT"][0] == "1"
