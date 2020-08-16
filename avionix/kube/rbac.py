from typing import List, Optional

from avionix.kube.base_objects import KubernetesBaseObject
from avionix.kube.meta import ListMeta
from avionix.kube.rbac_authorization import (
    ClusterRole,
    ClusterRoleBinding,
    Role,
    RoleBinding,
)


class RoleBindingList(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata.
    :param items: Items is a list of RoleBindings
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[RoleBinding],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class RoleList(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata.
    :param items: Items is a list of Roles
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self, metadata: ListMeta, items: List[Role], api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class ClusterRoleBindingList(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata.
    :param items: Items is a list of ClusterRoleBindings
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[ClusterRoleBinding],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class ClusterRoleList(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata.
    :param items: Items is a list of ClusterRoles
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[ClusterRole],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items
