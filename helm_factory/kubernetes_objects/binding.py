from typing import Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.metadata import ObjectMeta
from helm_factory.kubernetes_objects.reference import ObjectReference


class Binding(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    :param target: The target object that you want to bind to the standard object.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        target: ObjectReference,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.target = target
