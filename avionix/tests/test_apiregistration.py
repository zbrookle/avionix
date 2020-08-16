import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.apiregistration import APIService, APIServiceSpec
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.fixture
def api_service():
    return APIService(ObjectMeta(name="v0.test"), APIServiceSpec("test", 1, "v0", 1),)


def test_create_api_service(chart_info, api_service):
    builder = ChartBuilder(chart_info, [api_service])
    with ChartInstallationContext(builder):
        api_service_info = kubectl_get("apiservices")
        assert api_service_info["NAME"][0] == "v0.test"
