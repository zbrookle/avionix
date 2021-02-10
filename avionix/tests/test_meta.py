from datetime import datetime

import pytest

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.errors import HelmError
from avionix.kube.core import ConfigMap
from avionix.kube.meta import (
    APIGroup,
    APIResource,
    GroupVersionForDiscovery,
    ManagedFieldsEntry,
    OwnerReference,
    StatusDetails,
)
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


may_not_be_valid_resource_decorator = pytest.mark.xfail(
    raises=HelmError, reason="Api Resource may not be able to be created"
)


@may_not_be_valid_resource_decorator
def test_api_resource(chart_info):
    builder = ChartBuilder(
        chart_info,
        [APIResource("test", None, None, None, None, None, None, None, None)],  # type: ignore
    )
    with ChartInstallationContext(builder):
        print(kubectl_get("apiresource"))


@may_not_be_valid_resource_decorator
def test_status_details(chart_info):
    builder = ChartBuilder(chart_info, [StatusDetails("test", None, None)])  # type: ignore
    with ChartInstallationContext(builder):
        print(kubectl_get("statusdetails"))


@may_not_be_valid_resource_decorator
@pytest.mark.parametrize(
    "api_group",
    [APIGroup("test", None, None, [GroupVersionForDiscovery("test", None)])],  # type: ignore
)
def test_api_group(chart_info, api_group: APIGroup):
    builder = ChartBuilder(chart_info, [api_group])
    with ChartInstallationContext(builder):
        print(kubectl_get("apigroup"))
