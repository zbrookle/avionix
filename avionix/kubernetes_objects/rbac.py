from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.meta import ListMeta
from avionix.kubernetes_objects.rbac_authorization import (ClusterRole,
                                                           ClusterRoleBinding,
                                                           Role, RoleBinding)


class ClusterRoleBindingList(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata.
    :type metadata: ListMeta
    :param items:Items is a list of ClusterRoleBindings
    :type items: List[ClusterRoleBinding]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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


class RoleBindingList(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata.
    :type metadata: ListMeta
    :param items:Items is a list of RoleBindings
    :type items: List[RoleBinding]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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


class ClusterRoleList(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata.
    :type metadata: ListMeta
    :param items:Items is a list of ClusterRoles
    :type items: List[ClusterRole]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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


class RoleList(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata.
    :type metadata: ListMeta
    :param items:Items is a list of Roles
    :type items: List[Role]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ListMeta, items: List[Role], api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items
