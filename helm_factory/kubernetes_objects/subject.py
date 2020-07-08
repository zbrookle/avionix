from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.metadata import ObjectMeta
from helm_factory.yaml.yaml_handling import HelmYaml


class ResourceAttributes(HelmYaml):
    """
    :param group: Group is the API Group of the Resource.  "*" means all.
    :param resource: Resource is one of the existing resource types.  "*" means all.
    :param subresource: Subresource is one of the existing resource types.  "" means \
        none.
    :param verb: Verb is a kubernetes resource API verb, like: get, list, watch, \
        create, update, delete, proxy.  "*" means all.
    :param version: Version is the API Version of the Resource.  "*" means all.
    :param name: Name is the name of the resource being requested for a "get" or \
        deleted for a "delete". "" (empty) means all.
    :param namespace: Namespace is the namespace of the action being requested.  \
        Currently, there is no distinction between no namespace and all namespaces "" \
        (empty) is defaulted for LocalSubjectAccessReviews "" (empty) is empty for \
        cluster-scoped resources "" (empty) means "all" for namespace scoped resources \
        from a SubjectAccessReview or SelfSubjectAccessReview
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
    :param path: Path is the URL path of the request
    :param verb: Verb is the standard HTTP verb
    """

    def __init__(self, path: str, verb: str):
        self.path = path
        self.verb = verb


class SelfSubjectAccessReviewSpec(HelmYaml):
    """
    :param non_resource_attributes: NonResourceAttributes describes information for a \
        non-resource access request
    :param resource_attributes: ResourceAuthorizationAttributes describes information \
        for a resource access request
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
    :param metadata: None
    :param spec: Spec holds information about the request being evaluated.  user and \
        groups must be empty
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
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
    :param namespace: Namespace to evaluate rules for. Required.
    """

    def __init__(self, namespace: Optional[str] = None):
        self.namespace = namespace


class ResourceRule(HelmYaml):
    """
    :param api_groups: APIGroups is the name of the APIGroup that contains the \
        resources.  If multiple API groups are specified, any action requested against \
        one of the enumerated resources in any API group will be allowed.  "*" means \
        all.
    :param resource_names: ResourceNames is an optional white list of names that the \
        rule applies to.  An empty set means that everything is allowed.  "*" means \
        all.
    :param verbs: Verb is a list of kubernetes resource API verbs, like: get, list, \
        watch, create, update, delete, proxy.  "*" means all.
    :param resources: Resources is a list of resources this rule applies to.  "*" \
        means all in the specified apiGroups.  "*/foo" represents the subresource \
        'foo' for all resources in the specified apiGroups.
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


class NonResourceRule(HelmYaml):
    """
    :param non_resource_urls: NonResourceURLs is a set of partial urls that a user \
        should have access to.  *s are allowed, but only as the full, final step in \
        the path.  "*" means all.
    :param verbs: Verb is a list of kubernetes non-resource API verbs, like: get, \
        post, put, delete, patch, head, options.  "*" means all.
    """

    def __init__(self, non_resource_urls: List[str], verbs: List[str]):
        self.nonResourceURLs = non_resource_urls
        self.verbs = verbs


class SubjectAccessReviewSpec(HelmYaml):
    """
    :param extra: Extra corresponds to the user.Info.GetExtra() method from the \
        authenticator.  Since that is input to the authorizer it needs a reflection \
        here.
    :param groups: Groups is the groups you're testing for.
    :param non_resource_attributes: NonResourceAttributes describes information for a \
        non-resource access request
    :param resource_attributes: ResourceAuthorizationAttributes describes information \
        for a resource access request
    :param uid: UID information about the requesting user.
    :param user: User is the user you're testing for. If you specify "User" but not \
        "Groups", then is it interpreted as "What if User were not a member of any \
        groups
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
    :param metadata: None
    :param spec: Spec holds information about the request being evaluated
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
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
    :param api_group: APIGroup holds the API group of the referenced subject. Defaults \
        to "" for ServiceAccount subjects. Defaults to "rbac.authorization.k8s.io" for \
        User and Group subjects.
    :param name: Name of the object being referenced.
    :param namespace: Namespace of the referenced object.  If the object kind is \
        non-namespace, such as "User" or "Group", and this value is not empty the \
        Authorizer should report an error.
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
    :param metadata: None
    :param spec: Spec holds information about the request being evaluated.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
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
    :param metadata: None
    :param spec: Spec holds information about the request being evaluated.  \
        spec.namespace must be equal to the namespace you made the request against.  \
        If empty, it is defaulted.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
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
