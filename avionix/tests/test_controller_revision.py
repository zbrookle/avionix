import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.apps import ControllerRevision
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
