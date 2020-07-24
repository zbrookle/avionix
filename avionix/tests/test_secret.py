import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.core import Secret
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def empty_secret():
    return Secret(ObjectMeta(name="test-secret"))


@pytest.fixture
def non_empty_secret():
    return Secret(ObjectMeta(name="test-secret"), {"secret_key": "test"})


def get_secret_info():
    info = kubectl_get("secrets")
    return info[info["NAME"] == "test-secret"].reset_index(drop=True)


def test_empty_secret(chart_info, test_folder, empty_secret):
    builder = ChartBuilder(chart_info, [empty_secret], test_folder)
    with ChartInstallationContext(builder):
        secret_info = get_secret_info()
        assert secret_info["NAME"][0] == "test-secret"
        assert secret_info["DATA"][0] == "0"


def test_non_empty_secret(chart_info, test_folder, non_empty_secret):
    builder = ChartBuilder(chart_info, [non_empty_secret], test_folder)
    with ChartInstallationContext(builder):
        secret_info = get_secret_info()
        assert secret_info["NAME"][0] == "test-secret"
        assert secret_info["DATA"][0] == "1"
