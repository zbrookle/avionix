from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.meta import ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class UserInfo(HelmYaml):
    """
    :param extra:Any additional information provided by the authenticator.
    :type extra: dict
    :param groups:The names of groups this user is a part of.
    :type groups: List[str]
    :param username:The name that uniquely identifies this user among all active \
        users.
    :type username: str
    :param uid:A unique value that identifies this user across time. If this user is \
        deleted and another user by the same name is added, they will have different \
        UIDs.
    :type uid: Optional[str]
    """

    def __init__(
        self, extra: dict, groups: List[str], username: str, uid: Optional[str] = None
    ):
        self.extra = extra
        self.groups = groups
        self.username = username
        self.uid = uid


class TokenReviewSpec(HelmYaml):
    """
    :param audiences:Audiences is a list of the identifiers that the resource server \
        presented with the token identifies as. Audience-aware token authenticators \
        will verify that the token was intended for at least one of the audiences in \
        this list. If no audiences are provided, the audience will default to the \
        audience of the Kubernetes apiserver.
    :type audiences: List[str]
    :param token:Token is the opaque bearer token.
    :type token: str
    """

    def __init__(self, audiences: List[str], token: str):
        self.audiences = audiences
        self.token = token


class TokenReview(KubernetesBaseObject):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:Spec holds information about the request being evaluated
    :type spec: TokenReviewSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: TokenReviewSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class BoundObjectReference(KubernetesBaseObject):
    """
    :param name:Name of the referent.
    :type name: str
    :param uid:UID of the referent.
    :type uid: Optional[str]
    :param api_version:API version of the referent.
    :type api_version: Optional[str]
    """

    def __init__(
        self, name: str, uid: Optional[str] = None, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.name = name
        self.uid = uid


class TokenRequestSpec(HelmYaml):
    """
    :param audiences:Audiences are the intendend audiences of the token. A recipient \
        of a token must identitfy themself with an identifier in the list of audiences \
        of the token, and otherwise should reject the token. A token issued for \
        multiple audiences may be used to authenticate against any of the audiences \
        listed but implies a high degree of trust between the target audiences.
    :type audiences: List[str]
    :param bound_object_ref:BoundObjectRef is a reference to an object that the token \
        will be bound to. The token will only be valid for as long as the bound object \
        exists. NOTE: The API server's TokenReview endpoint will validate the \
        BoundObjectRef, but other audiences may not. Keep ExpirationSeconds small if \
        you want prompt revocation.
    :type bound_object_ref: BoundObjectReference
    :param expiration_seconds:ExpirationSeconds is the requested duration of validity \
        of the request. The token issuer may return a token with a different validity \
        duration so a client needs to check the 'expiration' field in a response.
    :type expiration_seconds: int
    """

    def __init__(
        self,
        audiences: List[str],
        bound_object_ref: BoundObjectReference,
        expiration_seconds: int,
    ):
        self.audiences = audiences
        self.boundObjectRef = bound_object_ref
        self.expirationSeconds = expiration_seconds


class TokenRequest(KubernetesBaseObject):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:None
    :type spec: TokenRequestSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: TokenRequestSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec