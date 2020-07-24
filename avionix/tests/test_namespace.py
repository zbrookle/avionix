import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.core import Namespace
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def namespace():
    return Namespace(ObjectMeta(name="test-namespace"))


def test_create_namespace(test_folder, chart_info, namespace):
    builder = ChartBuilder(chart_info, [namespace], test_folder)
    with ChartInstallationContext(builder):
        namespace_info = kubectl_get("namespaces")
        assert "test-namespace" in namespace_info["NAME"].values
