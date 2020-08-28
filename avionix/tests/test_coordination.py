import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.coordination import Lease, LeaseSpec
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.mark.parametrize("holder_identity", [None, "someone"])
def test_lease(chart_info, holder_identity):
    builder = ChartBuilder(
        chart_info,
        [
            Lease(
                ObjectMeta(name="test-lease"),
                LeaseSpec(holder_identity=holder_identity),
            )
        ],
    )
    with ChartInstallationContext(builder):
        lease_info = kubectl_get("lease")
        assert lease_info["NAME"][0] == "test-lease"
        assert lease_info["HOLDER"][0] == (holder_identity if holder_identity else "")
