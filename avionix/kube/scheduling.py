from typing import List, Optional

from avionix.kube.base_objects import KubernetesBaseObject
from avionix.kube.meta import ListMeta, ObjectMeta


class PriorityClass(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param global_default: globalDefault specifies whether this PriorityClass should be \
        considered as the default priority for pods that do not have any priority \
        class. Only one PriorityClass can be marked as `globalDefault`. However, if \
        more than one PriorityClasses exists with their `globalDefault` field set to \
        true, the smallest value of such global default PriorityClasses will be used \
        as the default priority.
    :param value: The value of this priority class. This is the actual priority that \
        pods receive when they have the name of this class in their pod spec.
    :param description: description is an arbitrary string that usually provides \
        guidelines on when this priority class should be used.
    :param preemption_policy: PreemptionPolicy is the Policy for preempting pods with \
        lower priority. One of Never, PreemptLowerPriority. Defaults to \
        PreemptLowerPriority if unset. This field is alpha-level and is only honored \
        by servers that enable the NonPreemptingPriority feature.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        global_default: bool,
        value: int,
        description: Optional[str] = None,
        preemption_policy: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.globalDefault = global_default
        self.value = value
        self.description = description
        self.preemptionPolicy = preemption_policy


class PriorityClassList(KubernetesBaseObject):
    """
    :param metadata: Standard list metadata More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param items: items is the list of PriorityClasses
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[PriorityClass],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items
