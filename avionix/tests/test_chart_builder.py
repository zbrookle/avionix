import pytest
from pathlib import Path
from avionix import ChartBuilder, ChartInfo
from avionix.tests.utils import get_test_deployment
from avionix.kubernetes_objects.deployment import Deployment
from tempfile import TemporaryDirectory
import os
import re

@pytest.fixture(scope="module")
def test_folder():
    return Path(__file__).parent


@pytest.fixture
def test_deployment():
    return get_test_deployment()


def test_chart_folder_building(test_deployment: Deployment, test_folder: Path):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(
            ChartInfo(api_version="3.2.4", name="test", version="0.1.0"),
            [test_deployment, test_deployment],
            output_directory=temp_folder
        )
        builder.generate_chart()
        temp_path = Path(temp_folder)
        templates_folder = temp_path / builder.chart_info.name / "templates"

        for file in os.listdir(templates_folder):
            with open(templates_folder / Path(file)) as kube_file:
                assert kube_file.read() == str(test_deployment)

            print(file)
            assert re.match(rf"{test_deployment.kind}-[0-9]+\.yaml", file)
