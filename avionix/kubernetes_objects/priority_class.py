from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta


class PriorityClass(KubernetesBaseObject):
    """
    :param description:description is an arbitrary string that usually provides \
        guidelines on when this priority class should be used.
    :type description: str
    :param global_default:globalDefault specifies whether this PriorityClass should be \
        considered as the default priority for pods that do not have any priority \
        class. Only one PriorityClass can be marked as `globalDefault`. However, if \
        more than one PriorityClasses exists with their `globalDefault` field set to \
        true, the smallest value of such global default PriorityClasses will be used \
        as the default priority.
    :type global_default: bool
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param value:The value of this priority class. This is the actual priority that \
        pods receive when they have the name of this class in their pod spec.
    :type value: int
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    :param preemption_policy:PreemptionPolicy is the Policy for preempting pods with \
        lower priority. One of Never, PreemptLowerPriority. Defaults to \
        PreemptLowerPriority if unset. This field is alpha-level and is only honored \
        by servers that enable the NonPreemptingPriority feature.
    :type preemption_policy: Optional[str]
    """

    def __init__(
        self,
        description: str,
        global_default: bool,
        metadata: ObjectMeta,
        value: int,
        api_version: Optional[str] = None,
        preemption_policy: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.description = description
        self.globalDefault = global_default
        self.metadata = metadata
        self.value = value
        self.preemptionPolicy = preemption_policy


class PriorityClassList(KubernetesBaseObject):
    """
    :param items:items is the list of PriorityClasses
    :type items: List[PriorityClass]
    :param metadata:Standard list metadata More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[PriorityClass],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
