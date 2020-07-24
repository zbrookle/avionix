import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.reference import ObjectReference
from avionix.kubernetes_objects.core import ServiceAccount
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def empty_service_account():
    return ServiceAccount(ObjectMeta(name="test-service-account"))


@pytest.fixture
def nonempty_service_account():
    return ServiceAccount(
        ObjectMeta(name="test-service-account"),
        secrets=[ObjectReference("test", name="test-ref")],
    )


def get_service_account_info():
    info = kubectl_get("serviceaccounts")
    return info[info["NAME"] != "default"].reset_index(drop=True)


def test_empty_service_account(chart_info, test_folder, empty_service_account):
    builder = ChartBuilder(chart_info, [empty_service_account], test_folder)
    with ChartInstallationContext(builder):
        service_account_info = get_service_account_info()
        assert service_account_info["NAME"][0] == "test-service-account"


def test_nonempty_service_account(chart_info, test_folder, nonempty_service_account):
    builder = ChartBuilder(chart_info, [nonempty_service_account], test_folder)
    with ChartInstallationContext(builder):
        service_account_info = get_service_account_info()
        assert service_account_info["NAME"][0] == "test-service-account"
        assert service_account_info["SECRETS"][0] == "2"
