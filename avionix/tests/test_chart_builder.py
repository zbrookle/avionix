import os
from pathlib import Path
import re
from tempfile import TemporaryDirectory

import pytest

from avionix import ChartBuilder, ChartInfo
from avionix.kubernetes_objects.deployment import Deployment
from avionix.tests.utils import (
    get_helm_installations,
    kubectl_get,
    ChartInstallationContext,
)


@pytest.fixture(scope="module")
def test_folder():
    return Path(__file__).parent


def test_chart_folder_building(test_deployment1: Deployment, test_folder: Path):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(
            ChartInfo(api_version="3.2.4", name="test", version="0.1.0"),
            [test_deployment1, test_deployment1],
            output_directory=temp_folder,
        )
        builder.generate_chart()
        temp_path = Path(temp_folder)
        templates_folder = temp_path / builder.chart_info.name / "templates"

        for file in os.listdir(templates_folder):
            with open(templates_folder / Path(file)) as kube_file:
                assert kube_file.read() == str(test_deployment1)

            assert re.match(rf"{test_deployment1.kind}-[0-9]+\.yaml", file)


def test_chart_installation(test_deployment1: Deployment, test_folder: Path):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(
            ChartInfo(
                api_version="3.2.4", name="test", version="0.1.0", app_version="v1"
            ),
            [test_deployment1],
            output_directory=temp_folder,
        )
        with ChartInstallationContext(builder):
            # Check helm release
            helm_installation = get_helm_installations()
            assert helm_installation["NAME"][0] == "test"
            assert helm_installation["REVISION"][0] == "1"
            assert helm_installation["STATUS"][0] == "deployed"

            deployments = kubectl_get("deployments")
            assert deployments["NAME"][0] == "test-deployment-1"
            assert deployments["READY"][0] == "1/1"

            pods = kubectl_get("pods")
            assert pods["READY"][0] == "1/1"
            assert pods["STATUS"][0] == "Running"

def test_intalling_two_components():
    pass
