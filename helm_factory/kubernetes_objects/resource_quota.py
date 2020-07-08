from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.metadata import ListMeta, ObjectMeta
from helm_factory.kubernetes_objects.selector import ScopeSelector
from helm_factory.yaml.yaml_handling import HelmYaml


class ResourceQuotaSpec(HelmYaml):
    """
    :param hard: hard is the set of desired hard limits for each named resource. More \
        info: https://kubernetes.io/docs/concepts/policy/resource-quotas/
    :param scope_selector: scopeSelector is also a collection of filters like scopes \
        that must match each object tracked by a quota but expressed using \
        ScopeSelectorOperator in combination with possible values. For a resource to \
        match, both scopes AND scopeSelector (if specified in spec), must be matched.
    :param scopes: A collection of filters that must match each object tracked by a \
        quota. If not specified, the quota matches all objects.
    """

    def __init__(
        self,
        hard: dict,
        scope_selector: Optional[ScopeSelector] = None,
        scopes: Optional[List[str]] = None,
    ):
        self.hard = hard
        self.scopeSelector = scope_selector
        self.scopes = scopes


class ResourceQuota(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    :param spec: Spec defines the desired quota. \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: ResourceQuotaSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class ResourceQuotaList(KubernetesBaseObject):
    """
    :param items: Items is a list of ResourceQuota objects. More info: \
        https://kubernetes.io/docs/concepts/policy/resource-quotas/
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        items: List[ResourceQuota],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
