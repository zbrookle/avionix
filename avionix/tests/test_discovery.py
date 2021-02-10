from pandas import DataFrame
import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.core import EndpointPort
from avionix.kube.discovery import Endpoint, EndpointConditions, EndpointSlice
from avionix.testing.helpers import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


def get_all_endpoint_ips(endpoint_slice: EndpointSlice) -> str:
    endpoint_ips = []
    for endpoint in endpoint_slice.endpoints:
        endpoint_ips += endpoint.addresses
    return ",".join(endpoint_ips)


def get_all_endpoint_ports(endpoint_slice: EndpointSlice) -> str:
    if endpoint_slice.ports is None:
        raise Exception("Endpoint port cannot be none!")
    return ",".join([str(port_object.port) for port_object in endpoint_slice.ports])


@pytest.mark.parametrize(
    "endpoint_slice",
    [
        EndpointSlice(
            ObjectMeta(name="endpoint-slice"),
            "IPv4",
            [Endpoint(["10.0.0.0", "10.0.0.1"])],
        ),
        EndpointSlice(
            ObjectMeta(name="endpoint-slice-w-conditions"),
            "IPv4",
            [Endpoint(["10.0.0.0", "10.0.0.1"], EndpointConditions(False))],
        ),
        EndpointSlice(
            ObjectMeta(name="endpoint-slice-w-conditions"),
            "IPv4",
            [Endpoint(["10.0.0.0", "10.0.0.1"])],
            [EndpointPort("http", "TCP", 80), EndpointPort("ssh", "TCP", 22)],
        ),
    ],
)
def test_endpoint_slice(chart_info, endpoint_slice: EndpointSlice):
    builder = ChartBuilder(chart_info, [endpoint_slice],)
    with ChartInstallationContext(builder):
        endpoint_slice_frame = DataFrame(kubectl_get("endpointslice"))
        endpoint_slice_frame = endpoint_slice_frame[
            endpoint_slice_frame["NAME"] == endpoint_slice.metadata.name
        ]
        assert endpoint_slice_frame["NAME"][0] == endpoint_slice.metadata.name
        assert endpoint_slice_frame["ADDRESSTYPE"][0] == endpoint_slice.addressType
        assert endpoint_slice_frame["PORTS"][0] == (
            "<unset>"
            if endpoint_slice.ports is None
            else get_all_endpoint_ports(endpoint_slice)
        )
        assert endpoint_slice_frame["ENDPOINTS"][0] == get_all_endpoint_ips(
            endpoint_slice
        )
