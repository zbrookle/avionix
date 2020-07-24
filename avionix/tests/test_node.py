import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.core import Node, NodeSpec
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def node_metadata():
    return ObjectMeta(name="test-node")


@pytest.fixture
def node(node_metadata):
    return Node(node_metadata, NodeSpec(external_id="12345", pod_cidr="10.0.0.0/24"))


def get_node_info():
    node_info = kubectl_get("nodes")
    return node_info[node_info["NAME"] != "minikube"].reset_index(drop=True)


def test_create_non_empty_node(test_folder, chart_info, node):
    builder = ChartBuilder(chart_info, [node], test_folder)
    with ChartInstallationContext(builder):
        node_info = get_node_info()
        assert node_info["NAME"][0] == "test-node"
        assert node_info["STATUS"][0] == "Unknown"
        assert node_info["VERSION"][0] == ""
