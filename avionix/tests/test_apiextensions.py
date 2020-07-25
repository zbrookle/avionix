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
from avionix.tests.utils import ChartInstallationContext, kubectl_get


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


def test_custom_resource(chart_info, custom_resource, test_folder):
    builder = ChartBuilder(chart_info, [custom_resource], test_folder)
    with ChartInstallationContext(builder):
        custom_resource_info = kubectl_get("customresourcedefinitions")
        assert custom_resource_info["NAME"][0] == "tests.customs.com"
