from pandas import DataFrame
import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.scheduling import PriorityClass
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.mark.parametrize(
    "priority_class",
    [
        PriorityClass(ObjectMeta(name="test-priority-class"), 1),
        PriorityClass(ObjectMeta(name="priority-class-global-default"), 1, True),
    ],
)
def test_priority_class(chart_info, priority_class):
    builder = ChartBuilder(chart_info, [priority_class])
    with ChartInstallationContext(builder):
        class_info = kubectl_get("priorityclass")
        class_info_frame = DataFrame(class_info)
        filter_frame = class_info_frame[
            class_info_frame["NAME"] == priority_class.metadata.name
        ].reset_index()
        assert filter_frame["NAME"][0] == priority_class.metadata.name
        assert filter_frame["VALUE"][0] == str(priority_class.value)
        assert (
            filter_frame["GLOBAL-DEFAULT"][0]
            == str(bool(priority_class.globalDefault)).lower()
        )
