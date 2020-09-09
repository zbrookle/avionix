import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.core import Toleration
from avionix.kube.node import Overhead, RuntimeClass, Scheduling
from avionix.testing.helpers import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.mark.parametrize(
    "runtime_class",
    [
        RuntimeClass(ObjectMeta(name="runtime-class"), "test"),
        RuntimeClass(
            ObjectMeta(name="runtime-class"),
            "test",
            scheduling=Scheduling([Toleration(operator="Exists")]),
        ),
        RuntimeClass(
            ObjectMeta(name="runtime-class"), "test", overhead=Overhead({"cpu": 2}),
        ),
    ],
)
def test_runtime_class(chart_info, runtime_class: RuntimeClass):
    builder = ChartBuilder(chart_info, [runtime_class],)
    with ChartInstallationContext(builder):
        runtime_class_info = kubectl_get("runtimeclass")
        assert runtime_class_info["NAME"][0] == runtime_class.metadata.name
        assert runtime_class_info["HANDLER"][0] == runtime_class.handler
