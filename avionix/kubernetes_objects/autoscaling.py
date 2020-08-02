from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.meta import ListMeta, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class CrossVersionObjectReference(KubernetesBaseObject):
    """
    :param name:Name of the referent; More info: \
        http://kubernetes.io/docs/user-guide/identifiers#names
    :type name: str
    :param api_version:API version of the referent
    :type api_version: Optional[str]
    """

    def __init__(self, name: str, api_version: Optional[str] = None):
        super().__init__(api_version)
        self.name = name


class HorizontalPodAutoscalerSpec(HelmYaml):
    """
    :param max_replicas:upper limit for the number of pods that can be set by the \
        autoscaler; cannot be smaller than MinReplicas.
    :type max_replicas: int
    :param scale_target_ref:reference to scaled resource; horizontal pod autoscaler \
        will learn the current resource consumption and will set the desired number of \
        pods by using its Scale subresource.
    :type scale_target_ref: CrossVersionObjectReference
    :param min_replicas:minReplicas is the lower limit for the number of replicas to \
        which the autoscaler can scale down.  It defaults to 1 pod.  minReplicas is \
        allowed to be 0 if the alpha feature gate HPAScaleToZero is enabled and at \
        least one Object or External metric is configured.  Scaling is active as long \
        as at least one metric value is available.
    :type min_replicas: Optional[int]
    :param target_cpuutilization_percentage:target average CPU utilization \
        (represented as a percentage of requested CPU) over all the pods; if not \
        specified the default autoscaling policy will be used.
    :type target_cpuutilization_percentage: Optional[int]
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


class HorizontalPodAutoscaler(KubernetesBaseObject):
    """
    :param metadata:Standard object metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:behaviour of autoscaler. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.  # noqa
    :type spec: HorizontalPodAutoscalerSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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


class HorizontalPodAutoscalerList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata.
    :type metadata: ListMeta
    :param items:list of horizontal pod autoscaler objects.
    :type items: List[HorizontalPodAutoscaler]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[HorizontalPodAutoscaler],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class Scale(KubernetesBaseObject):
    """
    :param metadata:Standard object metadata; More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.  # noqa
    :type metadata: ObjectMeta
    :param spec:defines the behavior of the scale. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.  # noqa
    :type spec: dict
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: dict, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec
