from avionix import ChartBuilder, ObjectMeta
from avionix.kube.autoscaling import (
    CrossVersionObjectReference,
    HorizontalPodAutoscaler,
    HorizontalPodAutoscalerSpec,
)
from avionix.testing.helpers import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


def test_horizontal_pod_autoscaler(chart_info):
    builder = ChartBuilder(
        chart_info,
        kubernetes_objects=[
            HorizontalPodAutoscaler(
                ObjectMeta(name="test-autoscaler"),
                HorizontalPodAutoscalerSpec(1, CrossVersionObjectReference("test")),
            )
        ],
    )
    with ChartInstallationContext(builder):
        autoscaling_info = kubectl_get("horizontalpodautoscaler")
        assert autoscaling_info["NAME"][0] == "test-autoscaler"
        assert autoscaling_info["REFERENCE"][0] == "CrossVersionObjectReference/test"
        assert autoscaling_info["MAXPODS"][0] == "1"
