import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.apps import DaemonSet, DaemonSetSpec
from avionix.tests.utils import ChartInstallationContext, kubectl_get


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
