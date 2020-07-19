from pathlib import Path
from tempfile import TemporaryDirectory

from avionix import ChartBuilder, ChartInfo
from avionix.kubernetes_objects.pod import Pod
from avionix.tests.utils import ChartInstallationContext, kubectl_get


def test_create_pod(chart_info: ChartInfo, test_folder: Path, pod: Pod):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [pod], temp_folder)
        with ChartInstallationContext(builder):
            pods_info = kubectl_get("pods")
            assert pods_info["NAME"][0] == "test-pod"
            assert pods_info["READY"][0] == "1/1"
            assert pods_info["STATUS"][0] == "Running"
