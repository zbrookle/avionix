import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.resource_quota import ResourceQuota, ResourceQuotaSpec
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def resource_quota():
    return ResourceQuota(
        ObjectMeta(name="test-resource-quota"), spec=ResourceQuotaSpec(hard={"cpu": 1})
    )


def test_resource_quota(chart_info, test_folder, resource_quota):
    builder = ChartBuilder(chart_info, [resource_quota], test_folder)
    with ChartInstallationContext(builder):
        quota_info = kubectl_get("resourcequotas")
        assert quota_info["NAME"][0] == "test-resource-quota"
        assert quota_info["REQUEST"][0] == "cpu: 0/1"
