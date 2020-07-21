from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kubernetes_objects.endpoint import (
    EndpointAddress,
    Endpoints,
    EndpointSubset,
)
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def endpoints_metadata():
    return ObjectMeta(name="test-endpoints")


@pytest.fixture
def endpoints_no_subset(endpoints_metadata):
    return Endpoints(endpoints_metadata)


@pytest.fixture()
def endpoints_with_subset(endpoints_metadata):
    return Endpoints(
        endpoints_metadata,
        subsets=[
            EndpointSubset(
                addresses=[EndpointAddress("local", "10.9.8.7", None)],
                not_ready_addresses=None,
                ports=None,
            )
        ],
    )


def get_endpoints_info():
    info = kubectl_get("endpoints")
    return info[info["NAME"] != "kubernetes"].reset_index(drop=True)


def test_endpoints_no_subset(
    chart_info: ChartInfo, test_folder, endpoints_no_subset: Endpoints
):
    builder = ChartBuilder(chart_info, [endpoints_no_subset], test_folder)
    with ChartInstallationContext(builder):
        endpoints_info = get_endpoints_info()
        assert endpoints_info["NAME"][0] == "test-endpoints"
        assert endpoints_info["ENDPOINTS"][0] == "<none>"


def test_endpoints_with_subset(
    chart_info: ChartInfo, test_folder, endpoints_with_subset: Endpoints
):
    builder = ChartBuilder(chart_info, [endpoints_with_subset], test_folder)
    with ChartInstallationContext(builder):
        endpoints_info = get_endpoints_info()
        assert endpoints_info["NAME"][0] == "test-endpoints"
        assert endpoints_info["ENDPOINTS"][0] == "10.9.8.7"
