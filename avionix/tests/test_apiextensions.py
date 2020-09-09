from typing import Optional

import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.apiextensions import (
    CustomResourceColumnDefinition,
    CustomResourceConversion,
    CustomResourceDefinition,
    CustomResourceDefinitionNames,
    CustomResourceDefinitionSpec,
    CustomResourceDefinitionVersion,
    CustomResourceSubresources,
    CustomResourceSubresourceScale,
    CustomResourceValidation,
    ExternalDocumentation,
    JSONSchemaProps,
    WebhookClientConfig,
    WebhookConversion,
)
from avionix.kube.apiregistration import ServiceReference
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


def get_custom_resource_definition(
    external_documentation: Optional[ExternalDocumentation] = None,
    subresources: Optional[CustomResourceSubresources] = None,
    custom_resource_conversion: Optional[CustomResourceConversion] = None,
):
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
                    CustomResourceValidation(
                        JSONSchemaProps("object", external_docs=external_documentation)
                    ),
                    False,
                    True,
                    subresources=subresources,
                )
            ],
            conversion=custom_resource_conversion,
        ),
    )


@pytest.mark.parametrize(
    "custom_resource",
    [
        get_custom_resource_definition(),
        get_custom_resource_definition(ExternalDocumentation("test.com")),
        get_custom_resource_definition(
            subresources=CustomResourceSubresources(
                CustomResourceSubresourceScale(".spec.test.test", ".status.test.test")
            )
        ),
        get_custom_resource_definition(
            custom_resource_conversion=CustomResourceConversion(
                WebhookConversion(
                    WebhookClientConfig(
                        service=ServiceReference("test-service", "default")
                    ),
                    ["v1"],
                ),
                "Webhook",
            )
        ),
    ],
)
def test_custom_resource(chart_info, custom_resource: CustomResourceDefinition):
    builder = ChartBuilder(chart_info, [custom_resource])
    with ChartInstallationContext(builder):
        custom_resource_info = kubectl_get("customresourcedefinitions")
        assert custom_resource_info["NAME"][0] == "tests.customs.com"
