from avionix.kube.node import RuntimeClass
from avionix.testing.installation_context import ChartInstallationContext
from avionix.testing.helpers import kubectl_get
from avionix import ChartBuilder, ObjectMeta


def test_runtime_class(chart_info):
    builder = ChartBuilder(
        chart_info, [RuntimeClass(ObjectMeta(name="runtime-class",
                                             namespace="default"), "test")],
    )
    with ChartInstallationContext(builder):
        runtime_class_info = kubectl_get("networkpolicy", "default")
        print(runtime_class_info)
        raise Exception
