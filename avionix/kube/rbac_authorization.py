"""
Contains classes related to Role Based Access Control
"""

from typing import List, Optional

from avionix.kube.base_objects import RbacAuthorization
from avionix.kube.meta import LabelSelector, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class PolicyRule(HelmYaml):
    """
    :param api_groups: APIGroups is the name of the APIGroup that contains the \
        resources.  If multiple API groups are specified, any action requested against \
        one of the enumerated resources in any API group will be allowed.
    :param resources: Resources is a list of resources this rule applies to.  \
        ResourceAll represents all resources.
    :param verbs: Verbs is a list of Verbs that apply to ALL the ResourceKinds and \
        AttributeRestrictions contained in this rule.  VerbAll represents all kinds.
    :param resource_names: ResourceNames is an optional white list of names that the \
        rule applies to.  An empty set means that everything is allowed.
    :param non_resource_urls: NonResourceURLs is a set of partial urls that a user \
        should have access to.  '*'s are allowed, but only as the full, final step in \
        the path Since non-resource URLs are not namespaced, this field is only \
        applicable for ClusterRoles referenced from a ClusterRoleBinding. Rules can \
        either apply to API resources (such as "pods" or "secrets") or non-resource \
        URL paths (such as "/api"),  but not both.
    """

    def __init__(
        self,
        api_groups: List[str],
        resources: List[str],
        verbs: List[str],
        resource_names: Optional[List[str]] = None,
        non_resource_urls: Optional[List[str]] = None,
    ):
        self.apiGroups = api_groups
        self.nonResourceURLs = non_resource_urls
        self.resourceNames = resource_names
        self.resources = resources
        self.verbs = verbs


class Role(RbacAuthorization):
    """
    :param metadata: Standard object's metadata.
    :param rules: Rules holds all the PolicyRules for this Role
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
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


class RoleRef(HelmYaml):
    """
    :param name: Name is the name of resource being referenced
    :param api_group: APIGroup is the group for the resource being referenced
    :param kind: Kind is the type of resource being referenced
    """

    def __init__(self, name: str, api_group: str, kind: str):
        self.name = name
        self.apiGroup = api_group
        self.kind = kind


class Subject(HelmYaml):
    """
    :param name: Name of the object being referenced.
    :param kind: Kind of object being referenced. Values defined by this API group are \
        "User", "Group", and "ServiceAccount". If the Authorizer does not recognized \
        the kind value, the Authorizer should report an error.
    :param api_group: APIGroup holds the API group of the referenced subject. Defaults \
        to "" for ServiceAccount subjects. Defaults to "rbac.authorization.k8s.io" for \
        User and Group subjects.
    :param namespace: Namespace of the referenced object.  If the object kind is \
        non-namespace, such as "User" or "Group", and this value is not empty the \
        Authorizer should report an error.
    """

    def __init__(
        self,
        name: str,
        kind: str,
        api_group: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        self.name = name
        self.kind = kind
        self.apiGroup = api_group
        self.namespace = namespace


class RoleBinding(RbacAuthorization):
    """
    :param metadata: Standard object's metadata.
    :param role_ref: RoleRef can reference a Role in the current namespace or a \
        ClusterRole in the global namespace. If the RoleRef cannot be resolved, the \
        Authorizer must return an error.
    :param subjects: Subjects holds references to the objects the role applies to.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        role_ref: RoleRef,
        subjects: Optional[List[Subject]] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.roleRef = role_ref
        self.subjects = subjects


class AggregationRule(HelmYaml):
    """
    :param cluster_role_selectors: ClusterRoleSelectors holds a list of selectors which \
        will be used to find ClusterRoles and create the rules. If any of the \
        selectors match, then the ClusterRole's permissions will be added
    """

    def __init__(self, cluster_role_selectors: List[LabelSelector]):
        self.clusterRoleSelectors = cluster_role_selectors


class ClusterRole(RbacAuthorization):
    """
    :param metadata: Standard object's metadata.
    :param aggregation_rule: AggregationRule is an optional field that describes how to \
        build the Rules for this ClusterRole. If AggregationRule is set, then the \
        Rules are controller managed and direct changes to Rules will be stomped by \
        the controller.
    :param rules: Rules holds all the PolicyRules for this ClusterRole
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        aggregation_rule: Optional[AggregationRule] = None,
        rules: Optional[List[PolicyRule]] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.aggregationRule = aggregation_rule
        self.rules = rules


class ClusterRoleBinding(RbacAuthorization):
    """
    :param metadata: Standard object's metadata.
    :param role_ref: RoleRef can only reference a ClusterRole in the global namespace. \
        If the RoleRef cannot be resolved, the Authorizer must return an error.
    :param subjects: Subjects holds references to the objects the role applies to.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        role_ref: RoleRef,
        subjects: Optional[List[Subject]] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.roleRef = role_ref
        self.subjects = subjects
