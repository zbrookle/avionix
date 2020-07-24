import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.core import LimitRange, LimitRangeItem, LimitRangeSpec
from avionix.tests.utils import ChartInstallationContext, kubectl_get


@pytest.fixture
def limit_range():
    return LimitRange(
        ObjectMeta(name="test-range"),
        LimitRangeSpec(limits=[LimitRangeItem({}, {}, {}, {}, "")]),
    )


def test_create_limitrange(test_folder, chart_info, limit_range):
    builder = ChartBuilder(chart_info, [limit_range], test_folder)
    with ChartInstallationContext(builder):
        namespace_info = kubectl_get("limitranges")
        assert namespace_info["NAME"][0] == "test-range"
