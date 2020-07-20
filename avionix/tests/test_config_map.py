from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kubernetes_objects.config_map import ConfigMap
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def config_map():
    return ConfigMap(ObjectMeta(name="test-config-map"), data={"my_test_value": "yes"})


def test_config_map(chart_info: ChartInfo, test_folder: Path, config_map: ConfigMap):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [config_map], temp_folder)
        with ChartInstallationContext(builder):
            config_maps = kubectl_get("configmaps")
            assert config_maps["NAME"][0] == "test-config-map"
            assert config_maps["DATA"][0] == "1"