from avionix import ChartBuilder, ObjectMeta
from avionix.kube.node import RuntimeClass
from avionix.testing.helpers import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


def test_runtime_class(chart_info):
    builder = ChartBuilder(
        chart_info, [RuntimeClass(ObjectMeta(name="runtime-class"), "test")],
    )
    with ChartInstallationContext(builder):
        kubectl_get("networkpolicy")
