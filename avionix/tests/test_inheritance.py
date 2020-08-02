import pytest

from avionix import ChartBuilder, ChartInfo
from avionix.kubernetes_objects.core import Event
from avionix.testing.installation_context import ChartInstallationContext
from avionix.tests.utils import get_event_info


@pytest.fixture
def my_event_object(object_meta_event, event_obj_ref):
    class MyEvent(Event):
        def __init__(self):
            super().__init__(
                metadata=object_meta_event,
                involved_object=event_obj_ref,
                message="test message",
                reason="testing",
                type="test-type",
            )

    return MyEvent()


def test_installing_from_child_class(chart_info, my_event_object):
    builder = ChartBuilder(
        ChartInfo(api_version="3.2.4", name="test", version="0.1.0", app_version="v1"),
        [my_event_object],
    )
    with ChartInstallationContext(builder):
        event_info = get_event_info()
        assert event_info["TYPE"][0] == "test-type"
        assert event_info["REASON"][0] == "testing"
        assert event_info["OBJECT"][0] == "objectreference/test-ref"
        assert event_info["MESSAGE"][0] == "test message"


def test_installing_from_child_class_with_extra_instance_vars(
    chart_info, my_event_object
):
    my_event_object._my_new_variable = "test"

    builder = ChartBuilder(
        ChartInfo(api_version="3.2.4", name="test", version="0.1.0", app_version="v1"),
        [my_event_object],
    )
    with ChartInstallationContext(builder):
        event_info = get_event_info()
        assert event_info["TYPE"][0] == "test-type"
        assert event_info["REASON"][0] == "testing"
        assert event_info["OBJECT"][0] == "objectreference/test-ref"
        assert event_info["MESSAGE"][0] == "test message"
