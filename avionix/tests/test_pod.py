from pathlib import Path
from tempfile import TemporaryDirectory

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kubernetes_objects.pod import Pod, PodTemplate, PodTemplateSpec
from avionix.tests.utils import ChartInstallationContext, kubectl_get

import pytest

def test_create_pod(chart_info: ChartInfo, test_folder: Path, pod: Pod):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [pod], temp_folder)
        with ChartInstallationContext(builder):
            pods_info = kubectl_get("pods")
            assert pods_info["NAME"][0] == "test-pod"
            assert pods_info["READY"][0] == "1/1"
            assert pods_info["STATUS"][0] == "Running"

@pytest.fixture
def pod_template(pod_spec):
    return PodTemplate(ObjectMeta(name="test-pod-template"), PodTemplateSpec(
        ObjectMeta(), pod_spec))

def test_create_pod_template(chart_info: ChartInfo, test_folder: Path, pod_template:
PodTemplate):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [pod_template], temp_folder)
        with ChartInstallationContext(builder):
            template_info = kubectl_get("podtemplates")
            assert template_info["NAME"][0] == "test-pod-template"
            assert template_info["CONTAINERS"][0] == "test-container-0"
            assert template_info["IMAGES"][0] == "k8s.gcr.io/echoserver:1.4"
