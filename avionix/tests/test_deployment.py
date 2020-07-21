import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.deployment import Deployment, DeploymentSpec
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def deployment(test_labels, pod_template_spec, selector):
    return Deployment(
        metadata=ObjectMeta(name="test-deployment", labels=test_labels),
        spec=DeploymentSpec(replicas=1, template=pod_template_spec, selector=selector,),
    )


def test_deployment(chart_info, test_folder, deployment):
    builder = ChartBuilder(chart_info, [deployment], test_folder)
    with ChartInstallationContext(builder):
        deployment_info = kubectl_get("deployments")
        assert deployment_info["NAME"][0] == "test-deployment"
        assert deployment_info["READY"][0] == "1/1"
