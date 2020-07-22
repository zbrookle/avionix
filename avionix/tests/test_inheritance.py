import pytest

from avionix import ChartBuilder, ObjectMeta, ChartInfo
from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.tests.utils import (
    ChartInstallationContext,
    kubectl_get,
)


@pytest.fixture
def my_deployment_object(selector, pod_template_spec, test_labels):
    class MyDeployment(Deployment):
        def __init__(self):
            super().__init__(
                metadata=ObjectMeta(name="test-deployment", labels=test_labels),
                spec=DeploymentSpec(
                    replicas=1, template=pod_template_spec, selector=selector,
                ),
            )

    return MyDeployment()


def test_installing_from_child_class(chart_info, my_deployment_object, test_folder):
    builder = ChartBuilder(
        ChartInfo(api_version="3.2.4", name="test", version="0.1.0", app_version="v1"),
        [my_deployment_object],
        test_folder,
    )
    with ChartInstallationContext(builder):
        deployments = kubectl_get("deployments")
        assert deployments["NAME"][0] == "test-deployment"
        assert deployments["READY"][0] == "1/1"

        pods = kubectl_get("pods")
        assert pods["READY"][0] == "1/1"
        assert pods["STATUS"][0] == "Running"
