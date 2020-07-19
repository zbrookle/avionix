from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kubernetes_objects.event import Event
from avionix.kubernetes_objects.reference import ObjectReference
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def non_empty_event():
    return Event(
        ObjectMeta(name="test-event"),
        ObjectReference("test-pod", name="test-ref"),
        message="test message",
        reason="testing",
        type="test-type",
    )


def test_create_nonempty_event(
    chart_info: ChartInfo, test_folder: Path, non_empty_event: Event
):
    with TemporaryDirectory(dir=test_folder) as temp_folder:
        builder = ChartBuilder(chart_info, [non_empty_event], temp_folder)
        with ChartInstallationContext(builder):
            event_info = kubectl_get("events")
            print(event_info)
            assert event_info["TYPE"][0] == "test-type"
            assert event_info["REASON"][0] == "testing"
            assert event_info["OBJECT"][0] == "/test-ref"
            assert event_info["MESSAGE"][0] == "test message"
