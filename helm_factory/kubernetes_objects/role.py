from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.metadata import ListMeta, ObjectMeta
from helm_factory.kubernetes_objects.selector import LabelSelector
from helm_factory.kubernetes_objects.subject import Subject
from helm_factory.yaml.yaml_handling import HelmYaml


class AggregationRule(HelmYaml):
    """
    :param cluster_role_selectors: ClusterRoleSelectors holds a list of selectors \
        which will be used to find ClusterRoles and create the rules. If any of the \
        selectors match, then the ClusterRole's permissions will be added
    """

    def __init__(self, cluster_role_selectors: List[LabelSelector]):
        self.clusterRoleSelectors = cluster_role_selectors


class PolicyRule(HelmYaml):
    """
    :param api_groups: APIGroups is the name of the APIGroup that contains the \
        resources.  If multiple API groups are specified, any action requested against \
        one of the enumerated resources in any API group will be allowed.
    :param non_resource_urls: NonResourceURLs is a set of partial urls that a user \
        should have access to.  *s are allowed, but only as the full, final step in \
        the path Since non-resource URLs are not namespaced, this field is only \
        applicable for ClusterRoles referenced from a ClusterRoleBinding. Rules can \
        either apply to API resources (such as "pods" or "secrets") or non-resource \
        URL paths (such as "/api"),  but not both.
    :param resource_names: ResourceNames is an optional white list of names that the \
        rule applies to.  An empty set means that everything is allowed.
    :param verbs: Verbs is a list of Verbs that apply to ALL the ResourceKinds and \
        AttributeRestrictions contained in this rule.  VerbAll represents all kinds.
    :param resources: Resources is a list of resources this rule applies to.  \
        ResourceAll represents all resources.
    """

    def __init__(
        self,
        api_groups: List[str],
        non_resource_urls: List[str],
        resource_names: List[str],
        verbs: List[str],
        resources: Optional[List[str]] = None,
    ):
        self.apiGroups = api_groups
        self.nonResourceURLs = non_resource_urls
        self.resourceNames = resource_names
        self.verbs = verbs
        self.resources = resources


class Role(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata.
    :param rules: Rules holds all the PolicyRules for this Role
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        rules: List[PolicyRule],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.rules = rules


class RoleRef(KubernetesBaseObject):
    """
    :param api_group: APIGroup is the group for the resource being referenced
    :param name: Name is the name of resource being referenced
    """

    def __init__(self, api_group: str, name: Optional[str] = None):
        self.apiGroup = api_group
        self.name = name


class RoleBinding(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata.
    :param role_ref: RoleRef can reference a Role in the current namespace or a \
        ClusterRole in the global namespace. If the RoleRef cannot be resolved, the \
        Authorizer must return an error.
    :param subjects: Subjects holds references to the objects the role applies to.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        role_ref: RoleRef,
        subjects: List[Subject],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.roleRef = role_ref
        self.subjects = subjects


class RoleBindingList(KubernetesBaseObject):
    """
    :param items: Items is a list of RoleBindings
    :param metadata: Standard object's metadata.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
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


class RoleList(KubernetesBaseObject):
    """
    :param items: Items is a list of Roles
    :param metadata: Standard object's metadata.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self, items: List[Role], metadata: ListMeta, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class ClusterRole(KubernetesBaseObject):
    """
    :param aggregation_rule: AggregationRule is an optional field that describes how \
        to build the Rules for this ClusterRole. If AggregationRule is set, then the \
        Rules are controller managed and direct changes to Rules will be stomped by \
        the controller.
    :param metadata: Standard object's metadata.
    :param rules: Rules holds all the PolicyRules for this ClusterRole
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        aggregation_rule: AggregationRule,
        metadata: ObjectMeta,
        rules: List[PolicyRule],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.aggregationRule = aggregation_rule
        self.metadata = metadata
        self.rules = rules


class ClusterRoleBinding(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata.
    :param role_ref: RoleRef can only reference a ClusterRole in the global namespace. \
        If the RoleRef cannot be resolved, the Authorizer must return an error.
    :param subjects: Subjects holds references to the objects the role applies to.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        role_ref: RoleRef,
        subjects: List[Subject],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.roleRef = role_ref
        self.subjects = subjects


class ClusterRoleBindingList(KubernetesBaseObject):
    """
    :param items: Items is a list of ClusterRoleBindings
    :param metadata: Standard object's metadata.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
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


class ClusterRoleList(KubernetesBaseObject):
    """
    :param items: Items is a list of ClusterRoles
    :param metadata: Standard object's metadata.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
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
