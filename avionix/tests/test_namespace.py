from tempfile import TemporaryDirectory

import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.namespace import Namespace
from avionix.tests.utils import ChartInstallationContext, kubectl_get

@pytest.fixture
def namespace():
    return Namespace(ObjectMeta(name="test-namespace"))

def test_create_namespace(test_folder, chart_info, namespace):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [namespace], temp_folder)
        with ChartInstallationContext(builder):
            namespace_info = kubectl_get("namespaces")
            assert "test-namespace" in namespace_info["NAME"].values
