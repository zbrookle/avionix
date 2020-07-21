import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.replication_controller import (
    ReplicationController,
    ReplicationControllerSpec,
)
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def replication_controller(pod_template_spec):
    return ReplicationController(
        ObjectMeta(name="test-replication-controller"),
        spec=ReplicationControllerSpec(pod_template_spec, selector={"type": "master"}),
    )


def test_replication_controller(chart_info, test_folder, replication_controller):
    builder = ChartBuilder(chart_info, [replication_controller])
    with ChartInstallationContext(builder):
        replication_info = kubectl_get("replicationcontrollers")
        print(replication_info)
        assert replication_info["NAME"][0] == "test-replication-controller"
        assert replication_info["DESIRED"][0] == "1"
        assert replication_info["CURRENT"][0] == "1"
