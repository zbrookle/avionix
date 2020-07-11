from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class ResourceAttributes(HelmYaml):
    """
    :param group:Group is the API Group of the Resource.  "*" means all.
    :type group: str
    :param resource:Resource is one of the existing resource types.  "*" means all.
    :type resource: str
    :param subresource:Subresource is one of the existing resource types.  "" means \
        none.
    :type subresource: str
    :param verb:Verb is a kubernetes resource API verb, like: get, list, watch, \
        create, update, delete, proxy.  "*" means all.
    :type verb: str
    :param version:Version is the API Version of the Resource.  "*" means all.
    :type version: str
    :param name:Name is the name of the resource being requested for a "get" or \
        deleted for a "delete". "" (empty) means all.
    :type name: Optional[str]
    :param namespace:Namespace is the namespace of the action being requested.  \
        Currently, there is no distinction between no namespace and all namespaces "" \
        (empty) is defaulted for LocalSubjectAccessReviews "" (empty) is empty for \
        cluster-scoped resources "" (empty) means "all" for namespace scoped resources \
        from a SubjectAccessReview or SelfSubjectAccessReview
    :type namespace: Optional[str]
    """

    def __init__(
        self,
        group: str,
        resource: str,
        subresource: str,
        verb: str,
        version: str,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        self.group = group
        self.resource = resource
        self.subresource = subresource
        self.verb = verb
        self.version = version
        self.name = name
        self.namespace = namespace


class NonResourceAttributes(HelmYaml):
    """
    :param path:Path is the URL path of the request
    :type path: str
    :param verb:Verb is the standard HTTP verb
    :type verb: str
    """

    def __init__(self, path: str, verb: str):
        self.path = path
        self.verb = verb


class SelfSubjectAccessReviewSpec(HelmYaml):
    """
    :param non_resource_attributes:NonResourceAttributes describes information for a \
        non-resource access request
    :type non_resource_attributes: NonResourceAttributes
    :param resource_attributes:ResourceAuthorizationAttributes describes information \
        for a resource access request
    :type resource_attributes: ResourceAttributes
    """

    def __init__(
        self,
        non_resource_attributes: NonResourceAttributes,
        resource_attributes: ResourceAttributes,
    ):
        self.nonResourceAttributes = non_resource_attributes
        self.resourceAttributes = resource_attributes


class SelfSubjectAccessReview(KubernetesBaseObject):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:Spec holds information about the request being evaluated.  user and \
        groups must be empty
    :type spec: SelfSubjectAccessReviewSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: SelfSubjectAccessReviewSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class SelfSubjectRulesReviewSpec(HelmYaml):
    """
    :param namespace:Namespace to evaluate rules for. Required.
    :type namespace: Optional[str]
    """

    def __init__(self, namespace: Optional[str] = None):
        self.namespace = namespace


class NonResourceRule(HelmYaml):
    """
    :param non_resource_urls:NonResourceURLs is a set of partial urls that a user \
        should have access to.  *s are allowed, but only as the full, final step in \
        the path.  "*" means all.
    :type non_resource_urls: List[str]
    :param verbs:Verb is a list of kubernetes non-resource API verbs, like: get, post, \
        put, delete, patch, head, options.  "*" means all.
    :type verbs: List[str]
    """

    def __init__(self, non_resource_urls: List[str], verbs: List[str]):
        self.nonResourceURLs = non_resource_urls
        self.verbs = verbs


class ResourceRule(HelmYaml):
    """
    :param api_groups:APIGroups is the name of the APIGroup that contains the \
        resources.  If multiple API groups are specified, any action requested against \
        one of the enumerated resources in any API group will be allowed.  "*" means \
        all.
    :type api_groups: List[str]
    :param resource_names:ResourceNames is an optional white list of names that the \
        rule applies to.  An empty set means that everything is allowed.  "*" means \
        all.
    :type resource_names: List[str]
    :param verbs:Verb is a list of kubernetes resource API verbs, like: get, list, \
        watch, create, update, delete, proxy.  "*" means all.
    :type verbs: List[str]
    :param resources:Resources is a list of resources this rule applies to.  "*" means \
        all in the specified apiGroups.  "*/foo" represents the subresource 'foo' for \
        all resources in the specified apiGroups.
    :type resources: Optional[List[str]]
    """

    def __init__(
        self,
        api_groups: List[str],
        resource_names: List[str],
        verbs: List[str],
        resources: Optional[List[str]] = None,
    ):
        self.apiGroups = api_groups
        self.resourceNames = resource_names
        self.verbs = verbs
        self.resources = resources


class SubjectAccessReviewSpec(HelmYaml):
    """
    :param extra:Extra corresponds to the user.Info.GetExtra() method from the \
        authenticator.  Since that is input to the authorizer it needs a reflection \
        here.
    :type extra: dict
    :param groups:Groups is the groups you're testing for.
    :type groups: List[str]
    :param non_resource_attributes:NonResourceAttributes describes information for a \
        non-resource access request
    :type non_resource_attributes: NonResourceAttributes
    :param resource_attributes:ResourceAuthorizationAttributes describes information \
        for a resource access request
    :type resource_attributes: ResourceAttributes
    :param uid:UID information about the requesting user.
    :type uid: str
    :param user:User is the user you're testing for. If you specify "User" but not \
        "Groups", then is it interpreted as "What if User were not a member of any \
        groups
    :type user: str
    """

    def __init__(
        self,
        extra: dict,
        groups: List[str],
        non_resource_attributes: NonResourceAttributes,
        resource_attributes: ResourceAttributes,
        uid: str,
        user: str,
    ):
        self.extra = extra
        self.groups = groups
        self.nonResourceAttributes = non_resource_attributes
        self.resourceAttributes = resource_attributes
        self.uid = uid
        self.user = user


class SubjectAccessReview(KubernetesBaseObject):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:Spec holds information about the request being evaluated
    :type spec: SubjectAccessReviewSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: SubjectAccessReviewSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class Subject(KubernetesBaseObject):
    """
    :param api_group:APIGroup holds the API group of the referenced subject. Defaults \
        to "" for ServiceAccount subjects. Defaults to "rbac.authorization.k8s.io" for \
        User and Group subjects.
    :type api_group: Optional[str]
    :param name:Name of the object being referenced.
    :type name: Optional[str]
    :param namespace:Namespace of the referenced object.  If the object kind is \
        non-namespace, such as "User" or "Group", and this value is not empty the \
        Authorizer should report an error.
    :type namespace: Optional[str]
    """

    def __init__(
        self,
        api_group: Optional[str] = None,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        self.apiGroup = api_group
        self.name = name
        self.namespace = namespace


class SelfSubjectRulesReview(KubernetesBaseObject):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:Spec holds information about the request being evaluated.
    :type spec: SelfSubjectRulesReviewSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: SelfSubjectRulesReviewSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class LocalSubjectAccessReview(KubernetesBaseObject):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:Spec holds information about the request being evaluated.  \
        spec.namespace must be equal to the namespace you made the request against.  \
        If empty, it is defaulted.
    :type spec: SubjectAccessReviewSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: SubjectAccessReviewSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec
