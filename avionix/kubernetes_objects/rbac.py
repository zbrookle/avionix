from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.meta import ListMeta
from avionix.kubernetes_objects.rbac_authorization import (
    ClusterRole,
    ClusterRoleBinding,
    Role,
    RoleBinding,
)


class ClusterRoleBindingList(KubernetesBaseObject):
    """
    :param items:Items is a list of ClusterRoleBindings
    :type items: List[ClusterRoleBinding]
    :param metadata:Standard object's metadata.
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[ClusterRoleBinding],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class RoleBindingList(KubernetesBaseObject):
    """
    :param items:Items is a list of RoleBindings
    :type items: List[RoleBinding]
    :param metadata:Standard object's metadata.
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[RoleBinding],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class ClusterRoleList(KubernetesBaseObject):
    """
    :param items:Items is a list of ClusterRoles
    :type items: List[ClusterRole]
    :param metadata:Standard object's metadata.
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[ClusterRole],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class RoleList(KubernetesBaseObject):
    """
    :param items:Items is a list of Roles
    :type items: List[Role]
    :param metadata:Standard object's metadata.
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, items: List[Role], metadata: ListMeta, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
