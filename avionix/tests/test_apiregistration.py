import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.apiregistration import APIService, APIServiceSpec
from avionix.testing import ChartInstallationContext, kubectl_get


@pytest.fixture
def api_service():
    return APIService(ObjectMeta(name="v0.test"), APIServiceSpec("test", 1, "v0", 1),)


def test_create_api_service(test_folder, chart_info, api_service):
    builder = ChartBuilder(chart_info, [api_service], test_folder)
    with ChartInstallationContext(builder):
        api_service_info = kubectl_get("apiservices")
        assert api_service_info["NAME"][0] == "v0.test"
