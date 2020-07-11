from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.selector import ScopeSelector
from avionix.yaml.yaml_handling import HelmYaml


class ResourceQuotaSpec(HelmYaml):
    """
    :param hard:hard is the set of desired hard limits for each named resource. More \
        info: https://kubernetes.io/docs/concepts/policy/resource-quotas/
    :type hard: dict
    :param scope_selector:scopeSelector is also a collection of filters like scopes \
        that must match each object tracked by a quota but expressed using \
        ScopeSelectorOperator in combination with possible values. For a resource to \
        match, both scopes AND scopeSelector (if specified in spec), must be matched.
    :type scope_selector: Optional[ScopeSelector]
    :param scopes:A collection of filters that must match each object tracked by a \
        quota. If not specified, the quota matches all objects.
    :type scopes: Optional[List[str]]
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
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the desired quota. \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: ResourceQuotaSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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
    :param items:Items is a list of ResourceQuota objects. More info: \
        https://kubernetes.io/docs/concepts/policy/resource-quotas/
    :type items: List[ResourceQuota]
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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
