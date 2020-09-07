from typing import Optional

import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.apps import (
    ControllerRevision,
    DaemonSet,
    DaemonSetSpec,
    DaemonSetUpdateStrategy,
    Deployment,
    DeploymentSpec,
    DeploymentStrategy,
    ReplicaSet,
    ReplicaSetSpec,
    RollingUpdateDaemonSet,
    RollingUpdateDeployment,
    RollingUpdateStatefulSetStrategy,
    StatefulSet,
    StatefulSetSpec,
    StatefulSetUpdateStrategy,
)
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.fixture
def controller_revision():
    return ControllerRevision(
        ObjectMeta(name="test-controller-revision"), {"test": "yes"}, 1
    )


def test_controller_revision(chart_info, controller_revision):
    builder = ChartBuilder(chart_info, [controller_revision])
    with ChartInstallationContext(builder):
        controller_revision_info = kubectl_get("controllerrevisions")
        assert controller_revision_info["NAME"][0] == "test-controller-revision"
        assert controller_revision_info["REVISION"][0] == "1"


@pytest.mark.parametrize(
    "update_strategy",
    [
        None,
        DaemonSetUpdateStrategy(type="OnDelete"),
        DaemonSetUpdateStrategy(RollingUpdateDaemonSet(2)),
    ],
)
def test_daemon_set(
    chart_info,
    pod_template_spec,
    selector,
    update_strategy: Optional[DaemonSetUpdateStrategy],
):
    builder = ChartBuilder(
        chart_info,
        [
            DaemonSet(
                ObjectMeta(name="test-daemon-set"),
                DaemonSetSpec(
                    pod_template_spec, selector, update_strategy=update_strategy
                ),
            )
        ],
    )
    with ChartInstallationContext(builder):
        daemon_set_info = kubectl_get("daemonsets")
        assert daemon_set_info["NAME"][0] == "test-daemon-set"
        assert daemon_set_info["DESIRED"][0] == "1"
        assert daemon_set_info["CURRENT"][0] == "1"


@pytest.mark.parametrize(
    "deployment_strategy",
    [
        None,
        DeploymentStrategy(type="Recreate"),
        DeploymentStrategy(RollingUpdateDeployment(2)),
    ],
)
def test_deployment(
    chart_info,
    test_labels,
    pod_template_spec,
    selector,
    deployment_strategy: Optional[DeploymentStrategy],
):
    builder = ChartBuilder(
        chart_info,
        [
            Deployment(
                metadata=ObjectMeta(name="test-deployment", labels=test_labels),
                spec=DeploymentSpec(
                    replicas=1,
                    template=pod_template_spec,
                    selector=selector,
                    strategy=deployment_strategy,
                ),
            )
        ],
    )
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


def test_replica_set(chart_info, replica_set):
    builder = ChartBuilder(chart_info, [replica_set])
    with ChartInstallationContext(builder):
        replica_set_info = kubectl_get("replicasets")
        assert replica_set_info["NAME"][0] == "test-replica-set"
        assert replica_set_info["DESIRED"][0] == "1"
        assert replica_set_info["CURRENT"][0] == "1"


@pytest.mark.parametrize(
    "update_strategy",
    [
        None,
        StatefulSetUpdateStrategy(None, type="OnDelete"),
        StatefulSetUpdateStrategy(RollingUpdateStatefulSetStrategy(1)),
    ],
)
def test_stateful_set(
    chart_info,
    pod_template_spec,
    selector,
    update_strategy: Optional[StatefulSetUpdateStrategy],
):
    builder = ChartBuilder(
        chart_info,
        [
            StatefulSet(
                ObjectMeta(name="test-stateful-set"),
                StatefulSetSpec(
                    pod_template_spec,
                    selector,
                    "my-service",
                    update_strategy=update_strategy,
                ),
            )
        ],
    )
    with ChartInstallationContext(builder):
        stateful_set_info = kubectl_get("statefulsets")
        assert stateful_set_info["NAME"][0] == "test-stateful-set"
        assert stateful_set_info["READY"][0] == "1/1"
