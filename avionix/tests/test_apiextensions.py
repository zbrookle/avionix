import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.apiextensions import (
    CustomResourceColumnDefinition,
    CustomResourceDefinition,
    CustomResourceDefinitionNames,
    CustomResourceDefinitionSpec,
    CustomResourceDefinitionVersion,
    CustomResourceValidation,
    JSONSchemaProps,
)
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.fixture
def custom_resource():
    return CustomResourceDefinition(
        ObjectMeta(name="tests.customs.com"),
        CustomResourceDefinitionSpec(
            "customs.com",
            CustomResourceDefinitionNames(["test"], "test-kind", "tests"),
            "Cluster",
            [
                CustomResourceDefinitionVersion(
                    "test-version",
                    [CustomResourceColumnDefinition("test-name", ".path", "integer")],
                    CustomResourceValidation(JSONSchemaProps("object",)),
                    False,
                    True,
                )
            ],
        ),
    )


def test_custom_resource(chart_info, custom_resource):
    builder = ChartBuilder(chart_info, [custom_resource])
    with ChartInstallationContext(builder):
        custom_resource_info = kubectl_get("customresourcedefinitions")
        assert custom_resource_info["NAME"][0] == "tests.customs.com"
