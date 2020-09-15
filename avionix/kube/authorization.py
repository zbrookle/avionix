"""
For the time being this will not be implemented as there is no helm support
"""
# from typing import List, Optional
#
# from avionix.kube.base_objects import Authorization
# from avionix.kube.meta import ObjectMeta
# from avionix.yaml.yaml_handling import HelmYaml
#
#
# class ResourceAttributes(HelmYaml):
#     """
#     :param name: Name is the name of the resource being requested for a "get" or \
#         deleted for a "delete". "" (empty) means all.
#     :param group: Group is the API Group of the Resource.  "*" means all.
#     :param resource: Resource is one of the existing resource types.  "*" means all.
#     :param subresource: Subresource is one of the existing resource types.  "" means \
#         none.
#     :param verb: Verb is a kubernetes resource API verb, like: get, list, watch, \
#         create, update, delete, proxy.  "*" means all.
#     :param version: Version is the API Version of the Resource.  "*" means all.
#     :param namespace: Namespace is the namespace of the action being requested.  \
#         Currently, there is no distinction between no namespace and all namespaces "" \
#         (empty) is defaulted for LocalSubjectAccessReviews "" (empty) is empty for \
#         cluster-scoped resources "" (empty) means "all" for namespace scoped resources \
#         from a SubjectAccessReview or SelfSubjectAccessReview
#     """
#
#     def __init__(
#         self,
#         name: str,
#         group: str,
#         resource: str,
#         subresource: str,
#         verb: str,
#         version: str,
#         namespace: Optional[str] = None,
#     ):
#         self.name = name
#         self.group = group
#         self.resource = resource
#         self.subresource = subresource
#         self.verb = verb
#         self.version = version
#         self.namespace = namespace
#
#
# class NonResourceAttributes(HelmYaml):
#     """
#     :param path: Path is the URL path of the request
#     :param verb: Verb is the standard HTTP verb
#     """
#
#     def __init__(self, path: str, verb: str):
#         self.path = path
#         self.verb = verb
#
#
# class SelfSubjectAccessReviewSpec(HelmYaml):
#     """
#     :param non_resource_attributes: NonResourceAttributes describes information for a \
#         non-resource access request
#     :param resource_attributes: ResourceAuthorizationAttributes describes information \
#         for a resource access request
#     """
#
#     def __init__(
#         self,
#         non_resource_attributes: NonResourceAttributes,
#         resource_attributes: ResourceAttributes,
#     ):
#         self.nonResourceAttributes = non_resource_attributes
#         self.resourceAttributes = resource_attributes
#
#
# class SelfSubjectAccessReview(Authorization):
#     """
#     :param metadata: None
#     :param spec: Spec holds information about the request being evaluated.  user and \
#         groups must be empty
#     :param api_version: APIVersion defines the versioned schema of this representation \
#         of an object. Servers should convert recognized schemas to the latest internal \
#         value, and may reject unrecognized values. More info: \
#         https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
#     """
#
#     def __init__(
#         self,
#         metadata: ObjectMeta,
#         spec: SelfSubjectAccessReviewSpec,
#         api_version: Optional[str] = None,
#     ):
#         super().__init__(api_version)
#         self.metadata = metadata
#         self.spec = spec
#
#
# class NonResourceRule(HelmYaml):
#     """
#     :param non_resource_urls: NonResourceURLs is a set of partial urls that a user \
#         should have access to.  *s are allowed, but only as the full, final step in \
#         the path.  "*" means all.
#     :param verbs: Verb is a list of kubernetes non-resource API verbs, like: get, post, \
#         put, delete, patch, head, options.  "*" means all.
#     """
#
#     def __init__(self, non_resource_urls: List[str], verbs: List[str]):
#         self.nonResourceURLs = non_resource_urls
#         self.verbs = verbs
#
#
# class ResourceRule(HelmYaml):
#     """
#     :param api_groups: APIGroups is the name of the APIGroup that contains the \
#         resources.  If multiple API groups are specified, any action requested against \
#         one of the enumerated resources in any API group will be allowed.  "*" means \
#         all.
#     :param resource_names: ResourceNames is an optional white list of names that the \
#         rule applies to.  An empty set means that everything is allowed.  "*" means \
#         all.
#     :param resources: Resources is a list of resources this rule applies to.  "*"
#         means all in the specified apiGroups.  "\*/foo" represents the subresource
#         'foo' for all resources in the specified apiGroups.
#     :param verbs: Verb is a list of kubernetes resource API verbs, like: get, list, \
#         watch, create, update, delete, proxy.  "*" means all.
#     """
#
#     def __init__(
#         self,
#         api_groups: List[str],
#         resource_names: List[str],
#         resources: List[str],
#         verbs: List[str],
#     ):
#         self.apiGroups = api_groups
#         self.resourceNames = resource_names
#         self.resources = resources
#         self.verbs = verbs
#
#
# class SubjectAccessReviewSpec(HelmYaml):
#     """
#     :param extra: Extra corresponds to the user.Info.GetExtra() method from the \
#         authenticator.  Since that is input to the authorizer it needs a reflection \
#         here.
#     :param groups: Groups is the groups you're testing for.
#     :param non_resource_attributes: NonResourceAttributes describes information for a \
#         non-resource access request
#     :param resource_attributes: ResourceAuthorizationAttributes describes information \
#         for a resource access request
#     :param user: User is the user you're testing for. If you specify "User" but not \
#         "Groups", then is it interpreted as "What if User were not a member of any \
#         groups
#     :param uid: UID information about the requesting user.
#     """
#
#     def __init__(
#         self,
#         extra: dict,
#         groups: List[str],
#         non_resource_attributes: NonResourceAttributes,
#         resource_attributes: ResourceAttributes,
#         user: str,
#         uid: Optional[str] = None,
#     ):
#         self.extra = extra
#         self.groups = groups
#         self.nonResourceAttributes = non_resource_attributes
#         self.resourceAttributes = resource_attributes
#         self.user = user
#         self.uid = uid
#
#
# class LocalSubjectAccessReview(Authorization):
#     """
#     :param metadata: None
#     :param spec: Spec holds information about the request being evaluated.  \
#         spec.namespace must be equal to the namespace you made the request against.  \
#         If empty, it is defaulted.
#     :param api_version: APIVersion defines the versioned schema of this representation \
#         of an object. Servers should convert recognized schemas to the latest internal \
#         value, and may reject unrecognized values. More info: \
#         https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
#     """
#
#     def __init__(
#         self,
#         metadata: ObjectMeta,
#         spec: SubjectAccessReviewSpec,
#         api_version: Optional[str] = None,
#     ):
#         super().__init__(api_version)
#         self.metadata = metadata
#         self.spec = spec
#
#
# class SelfSubjectRulesReviewSpec(HelmYaml):
#     """
#     :param namespace: Namespace to evaluate rules for. Required.
#     """
#
#     def __init__(self, namespace: Optional[str] = None):
#         self.namespace = namespace
#
#
# class SelfSubjectRulesReview(Authorization):
#     """
#     :param metadata: None
#     :param spec: Spec holds information about the request being evaluated.
#     :param api_version: APIVersion defines the versioned schema of this representation \
#         of an object. Servers should convert recognized schemas to the latest internal \
#         value, and may reject unrecognized values. More info: \
#         https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
#     """
#
#     def __init__(
#         self,
#         metadata: ObjectMeta,
#         spec: SelfSubjectRulesReviewSpec,
#         api_version: Optional[str] = None,
#     ):
#         super().__init__(api_version)
#         self.metadata = metadata
#         self.spec = spec
#
#
# class SubjectAccessReview(Authorization):
#     """
#     :param metadata: None
#     :param spec: Spec holds information about the request being evaluated
#     :param api_version: APIVersion defines the versioned schema of this representation \
#         of an object. Servers should convert recognized schemas to the latest internal \
#         value, and may reject unrecognized values. More info: \
#         https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
#     """
#
#     def __init__(
#         self,
#         metadata: ObjectMeta,
#         spec: SubjectAccessReviewSpec,
#         api_version: Optional[str] = None,
#     ):
#         super().__init__(api_version)
#         self.metadata = metadata
#         self.spec = spec
