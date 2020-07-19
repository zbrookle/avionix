from pathlib import Path

import pytest

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.tests.utils import ChartInstallationContext, kubectl_get, get_test_container
from avionix.kubernetes_objects.pod import Pod, PodSpec
from tempfile import TemporaryDirectory

@pytest.fixture
def pod():
    return Pod(ObjectMeta(name="test-pod"), spec=PodSpec([get_test_container(0)]))

def test_create_pod(chart_info: ChartInfo, test_folder: Path, pod: Pod):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [pod], temp_folder)
        with ChartInstallationContext(builder):
            pods_info = kubectl_get("pods")
            assert pods_info["NAME"][0] == "test-pod"
            assert pods_info["READY"][0] == "1/1"
            assert pods_info["STATUS"][0] == "Running"