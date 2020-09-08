from datetime import datetime

import pytest

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kube.core import ConfigMap
from avionix.kube.meta import ManagedFieldsEntry, OwnerReference
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.mark.parametrize(
    "object_meta",
    [
        ObjectMeta(
            name="test-managed-fields",
            managed_fields=[
                ManagedFieldsEntry("test"),
                ManagedFieldsEntry(fields_v1={"my": "data"}),
                ManagedFieldsEntry(time=datetime.now()),
            ],
        ),
        ObjectMeta(
            name="test-owner-reference",
            owner_references=[OwnerReference("test", "10")],
        ),
    ],
)
def test_object_meta(chart_info: ChartInfo, object_meta: ObjectMeta):
    config_map = ConfigMap(object_meta, {"test": "1"},)
    builder = ChartBuilder(chart_info, [config_map])
    with ChartInstallationContext(builder):
        config_maps = kubectl_get("configmaps")
        assert config_maps["NAME"][0] == config_map.metadata.name
        assert config_maps["DATA"][0] == str(len(config_map.data))
