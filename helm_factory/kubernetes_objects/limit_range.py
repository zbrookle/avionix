from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.metadata import ListMeta, ObjectMeta
from helm_factory.yaml.yaml_handling import HelmYaml


class LimitRangeItem(HelmYaml):
    """
    :param default: Default resource requirement limit value by resource name if \
        resource limit is omitted.
    :param default_request: DefaultRequest is the default resource requirement request \
        value by resource name if resource request is omitted.
    :param max: Max usage constraints on this kind by resource name.
    :param min: Min usage constraints on this kind by resource name.
    :param type: Type of resource that this limit applies to.
    :param max_limit_request_ratio: MaxLimitRequestRatio if specified, the named \
        resource must have a request and limit that are both non-zero where limit \
        divided by request is less than or equal to the enumerated value; this \
        represents the max burst for the named resource.
    """

    def __init__(
        self,
        default: dict,
        default_request: dict,
        max: dict,
        min: dict,
        type: str,
        max_limit_request_ratio: Optional[dict] = None,
    ):
        self.default = default
        self.defaultRequest = default_request
        self.max = max
        self.min = min
        self.type = type
        self.maxLimitRequestRatio = max_limit_request_ratio


class LimitRangeSpec(HelmYaml):
    """
    :param limits: Limits is the list of LimitRangeItem objects that are enforced.
    """

    def __init__(self, limits: List[LimitRangeItem]):
        self.limits = limits


class LimitRange(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    :param spec: Spec defines the limits enforced. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: LimitRangeSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class LimitRangeList(KubernetesBaseObject):
    """
    :param items: Items is a list of LimitRange objects. More info: \
        https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        items: List[LimitRange],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
