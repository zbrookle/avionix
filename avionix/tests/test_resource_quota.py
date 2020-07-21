from tempfile import TemporaryDirectory

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
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [resource_quota], temp_folder)
        with ChartInstallationContext(builder):
            quota_info = kubectl_get("resourcequotas")
            print()
            print(quota_info)
            assert quota_info["NAME"][0] == "test-resource-quota"
            assert quota_info["REQUEST"][0] == "cpu: 0/1"
