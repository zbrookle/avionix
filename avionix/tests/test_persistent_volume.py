from tempfile import TemporaryDirectory

import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.volume import (
    PersistentVolume,
    PersistentVolumeClaim,
    PersistentVolumeSpec,
    HostPathVolumeSource,
)
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def persistent_volume():
    return PersistentVolume(
        ObjectMeta(name="test-persistent-volume"),
        PersistentVolumeSpec(
            ["ReadOnlyMany", "ReadWriteMany"],
            capacity={"storage": 1},
            host_path=HostPathVolumeSource("/home/test/tmp"),
        ),
    )


def test_persistent_volume(test_folder, chart_info, persistent_volume):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [persistent_volume], temp_folder)
        with ChartInstallationContext(builder):
            volume_info = kubectl_get("persistentvolumes")
            assert volume_info["NAME"][0] == "test-persistent-volume"
            assert volume_info["CAPACITY"][0] == "1"
