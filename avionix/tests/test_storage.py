import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.storage import (
    CSINode,
    CSIDriver,
    CSIDriverSpec,
    StorageClass,
    VolumeAttachment,
)
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext
from pandas import DataFrame


@pytest.mark.parametrize(
    "driver",
    [
        CSIDriver(
            ObjectMeta(name="test-driver-lifecycle"),
            CSIDriverSpec(volume_lifecycle_modes=["Ephemeral"]),
        ),
        CSIDriver(ObjectMeta(name="test-driver-attach"), CSIDriverSpec(False),),
    ],
)
def test_csi_driver(chart_info, driver: CSIDriver):
    builder = ChartBuilder(chart_info, [driver])
    with ChartInstallationContext(builder):
        driver_info = kubectl_get("csidriver")
        assert driver_info["NAME"][0] == driver.metadata.name
        assert (
            driver_info["ATTACHREQUIRED"][0]
            == str(bool(driver.spec.attachRequired)).lower()
            if driver.spec.attachRequired is not None
            else "true"
        )
        assert driver_info["MODES"][0] == (
            driver.spec.volumeLifecycleModes[0]
            if driver.spec.volumeLifecycleModes
            else "Persistent"
        )
