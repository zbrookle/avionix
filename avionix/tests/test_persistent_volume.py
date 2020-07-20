from tempfile import TemporaryDirectory

import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.volume import (
    PersistentVolume,
    PersistentVolumeClaim,
    PersistentVolumeClaimSpec,
    PersistentVolumeSpec,
    HostPathVolumeSource,
    ResourceRequirements,
)
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def access_modes():
    return ["ReadOnlyMany", "ReadWriteMany"]


modes_expected_value = "ROX,RWX"


@pytest.fixture
def persistent_volume(access_modes):
    return PersistentVolume(
        ObjectMeta(name="test-persistent-volume"),
        PersistentVolumeSpec(
            access_modes,
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
            assert volume_info["ACCESS MODES"][0] == modes_expected_value


@pytest.fixture
def empty_persistent_volume_claim(access_modes):
    return PersistentVolumeClaim(
        ObjectMeta(name="test-persistent-volume-claim"),
        PersistentVolumeClaimSpec(
            access_modes, ResourceRequirements(requests={"storage": 1}),
        ),
    )

def test_empty_persistent_volume_claim(
    test_folder, chart_info, empty_persistent_volume_claim
):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [empty_persistent_volume_claim], temp_folder)
        with ChartInstallationContext(builder):
            volume_info = kubectl_get("persistentvolumeclaims")
            assert volume_info["NAME"][0] == "test-persistent-volume-claim"
            assert volume_info["CAPACITY"][0] == "1"
            assert volume_info["ACCESS MODES"][0] == modes_expected_value
