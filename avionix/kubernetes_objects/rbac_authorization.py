from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.meta import LabelSelector, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class Subject(KubernetesBaseObject):
    """
    :param name:Name of the object being referenced.
    :type name: str
    :param api_group:APIGroup holds the API group of the referenced subject. Defaults \
        to "" for ServiceAccount subjects. Defaults to "rbac.authorization.k8s.io" for \
        User and Group subjects.
    :type api_group: Optional[str]
    :param namespace:Namespace of the referenced object.  If the object kind is \
        non-namespace, such as "User" or "Group", and this value is not empty the \
        Authorizer should report an error.
    :type namespace: Optional[str]
    """

    def __init__(
        self,
        name: str,
        api_group: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        self.name = name
        self.apiGroup = api_group
        self.namespace = namespace


class RoleRef(KubernetesBaseObject):
    """
    :param name:Name is the name of resource being referenced
    :type name: str
    :param api_group:APIGroup is the group for the resource being referenced
    :type api_group: str
    """

    def __init__(self, name: str, api_group: str):
        self.name = name
        self.apiGroup = api_group


class ClusterRoleBinding(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata.
    :type metadata: ObjectMeta
    :param role_ref:RoleRef can only reference a ClusterRole in the global namespace. \
        If the RoleRef cannot be resolved, the Authorizer must return an error.
    :type role_ref: RoleRef
    :param subjects:Subjects holds references to the objects the role applies to.
    :type subjects: List[Subject]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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


class RoleBinding(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata.
    :type metadata: ObjectMeta
    :param role_ref:RoleRef can reference a Role in the current namespace or a \
        ClusterRole in the global namespace. If the RoleRef cannot be resolved, the \
        Authorizer must return an error.
    :type role_ref: RoleRef
    :param subjects:Subjects holds references to the objects the role applies to.
    :type subjects: List[Subject]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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


class PolicyRule(HelmYaml):
    """
    :param api_groups:APIGroups is the name of the APIGroup that contains the \
        resources.  If multiple API groups are specified, any action requested against \
        one of the enumerated resources in any API group will be allowed.
    :type api_groups: List[str]
    :param non_resource_urls:NonResourceURLs is a set of partial urls that a user \
        should have access to.  *s are allowed, but only as the full, final step in \
        the path Since non-resource URLs are not namespaced, this field is only \
        applicable for ClusterRoles referenced from a ClusterRoleBinding. Rules can \
        either apply to API resources (such as "pods" or "secrets") or non-resource \
        URL paths (such as "/api"),  but not both.
    :type non_resource_urls: List[str]
    :param resource_names:ResourceNames is an optional white list of names that the \
        rule applies to.  An empty set means that everything is allowed.
    :type resource_names: List[str]
    :param resources:Resources is a list of resources this rule applies to.  \
        ResourceAll represents all resources.
    :type resources: List[str]
    :param verbs:Verbs is a list of Verbs that apply to ALL the ResourceKinds and \
        AttributeRestrictions contained in this rule.  VerbAll represents all kinds.
    :type verbs: List[str]
    """

    def __init__(
        self,
        api_groups: List[str],
        non_resource_urls: List[str],
        resource_names: List[str],
        resources: List[str],
        verbs: List[str],
    ):
        self.apiGroups = api_groups
        self.nonResourceURLs = non_resource_urls
        self.resourceNames = resource_names
        self.resources = resources
        self.verbs = verbs


class Role(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata.
    :type metadata: ObjectMeta
    :param rules:Rules holds all the PolicyRules for this Role
    :type rules: List[PolicyRule]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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


class AggregationRule(HelmYaml):
    """
    :param cluster_role_selectors:ClusterRoleSelectors holds a list of selectors which \
        will be used to find ClusterRoles and create the rules. If any of the \
        selectors match, then the ClusterRole's permissions will be added
    :type cluster_role_selectors: List[LabelSelector]
    """

    def __init__(self, cluster_role_selectors: List[LabelSelector]):
        self.clusterRoleSelectors = cluster_role_selectors


class ClusterRole(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata.
    :type metadata: ObjectMeta
    :param aggregation_rule:AggregationRule is an optional field that describes how to \
        build the Rules for this ClusterRole. If AggregationRule is set, then the \
        Rules are controller managed and direct changes to Rules will be stomped by \
        the controller.
    :type aggregation_rule: AggregationRule
    :param rules:Rules holds all the PolicyRules for this ClusterRole
    :type rules: List[PolicyRule]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        aggregation_rule: AggregationRule,
        rules: List[PolicyRule],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.aggregationRule = aggregation_rule
        self.rules = rules
