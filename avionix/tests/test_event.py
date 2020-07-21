import pytest

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kubernetes_objects.event import Event
from avionix.kubernetes_objects.reference import ObjectReference
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def object_meta_event():
    return ObjectMeta(name="test-event")


@pytest.fixture
def event_obj_ref():
    return ObjectReference("test-pod", name="test-ref")


@pytest.fixture
def empty_event(object_meta_event, event_obj_ref):
    return Event(object_meta_event, event_obj_ref)


@pytest.fixture
def non_empty_event(object_meta_event, event_obj_ref):
    return Event(
        object_meta_event,
        event_obj_ref,
        message="test message",
        reason="testing",
        type="test-type",
    )


def get_event_info():
    info = kubectl_get("events")
    return info[(info["TYPE"] != "Normal") & (info["TYPE"] != "Warning")].reset_index(
        drop=True
    )


def test_create_empty_event(chart_info: ChartInfo, test_folder, empty_event: Event):
    builder = ChartBuilder(chart_info, [empty_event], test_folder)
    with ChartInstallationContext(builder):
        event_info = get_event_info()
        print(event_info)
        assert event_info["TYPE"][0] == ""
        assert event_info["REASON"][0] == ""
        assert event_info["OBJECT"][0] == "/test-ref"
        assert event_info["MESSAGE"][0] == ""


def test_create_nonempty_event(
    chart_info: ChartInfo, test_folder, non_empty_event: Event
):
    builder = ChartBuilder(chart_info, [non_empty_event], test_folder)
    with ChartInstallationContext(builder):
        event_info = get_event_info()
        assert event_info["TYPE"][0] == "test-type"
        assert event_info["REASON"][0] == "testing"
        assert event_info["OBJECT"][0] == "/test-ref"
        assert event_info["MESSAGE"][0] == "test message"
