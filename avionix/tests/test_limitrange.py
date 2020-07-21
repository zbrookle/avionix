from tempfile import TemporaryDirectory

import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.limit_range import (
    LimitRange,
    LimitRangeItem,
    LimitRangeSpec,
)
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def empty_limit_range():
    return LimitRange(ObjectMeta(name="test-range"))


@pytest.fixture
def nonempty_limit_range():
    return LimitRange(
        ObjectMeta(name="test-range"),
        LimitRangeSpec(limits=[LimitRangeItem({}, {}, {}, {}, "")]),
    )


def test_create_empty_limitrange(test_folder, chart_info, empty_limit_range):
    builder = ChartBuilder(chart_info, [empty_limit_range], test_folder)
    with ChartInstallationContext(builder):
        namespace_info = kubectl_get("limitranges")
        assert namespace_info["NAME"][0] == "test-range"


def test_create_limitrange(test_folder, chart_info, nonempty_limit_range):
    builder = ChartBuilder(chart_info, [nonempty_limit_range], test_folder)
    with ChartInstallationContext(builder):
        namespace_info = kubectl_get("limitranges")
        assert namespace_info["NAME"][0] == "test-range"
