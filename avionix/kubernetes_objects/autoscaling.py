from typing import Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ObjectMeta


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
