import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.service import Service, ServiceSpec, ServicePort
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def empty_service():
    return Service(ObjectMeta(name="test-service"), ServiceSpec([ServicePort(80)]))


@pytest.fixture
def nonempty_service():
    return Service(
        ObjectMeta(name="test-service"),
        ServiceSpec(
            [
                ServicePort(80, name="port1"),
                ServicePort(8080, protocol="UDP", name="port2"),
            ], external_ips=["152.0.0.0"]
        ),
    )


def get_service_info():
    info = kubectl_get("services")
    return info[info["NAME"] != "kubernetes"].reset_index(drop=True)


def test_empty_service(chart_info, test_folder, empty_service):
    builder = ChartBuilder(chart_info, [empty_service], test_folder)
    with ChartInstallationContext(builder):
        service_info = get_service_info()
        assert service_info["NAME"][0] == "test-service"
        assert service_info["PORT(S)"][0] == "80/TCP"


def test_nonempty_service(chart_info, test_folder, nonempty_service):
    builder = ChartBuilder(chart_info, [nonempty_service], test_folder)
    with ChartInstallationContext(builder):
        service_info = get_service_info()
        assert service_info["NAME"][0] == "test-service"
        assert service_info["PORT(S)"][0] == '80/TCP,8080/UDP'
        assert service_info["EXTERNAL-IP"][0] == "152.0.0.0"
