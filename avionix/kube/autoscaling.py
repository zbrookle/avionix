"""
Classes related to scaling Kubernetes pods
"""

from typing import Optional

from avionix.kube.base_objects import Autoscaling
from avionix.kube.meta import ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class CrossVersionObjectReference(Autoscaling):
    """
    :param name: Name of the referent; More info: \
        http://kubernetes.io/docs/user-guide/identifiers#names
    :param api_version: API version of the referent
    """

    def __init__(self, name: str, api_version: Optional[str] = None):
        super().__init__(api_version)
        self.name = name


class HorizontalPodAutoscalerSpec(HelmYaml):
    """
    :param max_replicas: upper limit for the number of pods that can be set by the \
        autoscaler; cannot be smaller than MinReplicas.
    :param scale_target_ref: reference to scaled resource; horizontal pod autoscaler \
        will learn the current resource consumption and will set the desired number of \
        pods by using its Scale subresource.
    :param min_replicas: minReplicas is the lower limit for the number of replicas to \
        which the autoscaler can scale down.  It defaults to 1 pod.  minReplicas is \
        allowed to be 0 if the alpha feature gate HPAScaleToZero is enabled and at \
        least one Object or External metric is configured.  Scaling is active as long \
        as at least one metric value is available.
    :param target_cpuutilization_percentage: target average CPU utilization \
        (represented as a percentage of requested CPU) over all the pods; if not \
        specified the default autoscaling policy will be used.
    """

    def __init__(
        self,
        max_replicas: int,
        scale_target_ref: CrossVersionObjectReference,
        min_replicas: Optional[int] = None,
        target_cpuutilization_percentage: Optional[int] = None,
    ):
        self.maxReplicas = max_replicas
        self.scaleTargetRef = scale_target_ref
        self.minReplicas = min_replicas
        self.targetCPUUtilizationPercentage = target_cpuutilization_percentage


class HorizontalPodAutoscaler(Autoscaling):
    """
    :param metadata: Standard object metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: behaviour of autoscaler. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.  # noqa
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: HorizontalPodAutoscalerSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec
