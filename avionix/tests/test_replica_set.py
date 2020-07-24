import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.apps import ReplicaSet, ReplicaSetSpec
from avionix.tests.utils import ChartInstallationContext, kubectl_get


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
