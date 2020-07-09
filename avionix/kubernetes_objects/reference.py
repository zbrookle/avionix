from typing import Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.yaml.yaml_handling import HelmYaml


class OwnerReference(KubernetesBaseObject):
    """
    :param controller:If true, this reference points to the managing controller.
    :type controller: bool
    :param uid:UID of the referent. More info: \
        http://kubernetes.io/docs/user-guide/identifiers#uids
    :type uid: str
    :param api_version:API version of the referent.
    :type api_version: Optional[str]
    :param block_owner_deletion:If true, AND if the owner has the "foregroundDeletion" \
        finalizer, then the owner cannot be deleted from the key-value store until \
        this reference is removed. Defaults to false. To set this field, a user needs \
        "delete" permission of the owner, otherwise 422 (Unprocessable Entity) will be \
        returned.
    :type block_owner_deletion: Optional[bool]
    :param name:Name of the referent. More info: \
        http://kubernetes.io/docs/user-guide/identifiers#names
    :type name: Optional[str]
    """

    def __init__(
        self,
        controller: bool,
        uid: str,
        api_version: Optional[str] = None,
        block_owner_deletion: Optional[bool] = None,
        name: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.controller = controller
        self.uid = uid
        self.blockOwnerDeletion = block_owner_deletion
        self.name = name


class BoundObjectReference(KubernetesBaseObject):
    """
    :param uid:UID of the referent.
    :type uid: str
    :param api_version:API version of the referent.
    :type api_version: Optional[str]
    :param name:Name of the referent.
    :type name: Optional[str]
    """

    def __init__(
        self, uid: str, api_version: Optional[str] = None, name: Optional[str] = None
    ):
        super().__init__(api_version)
        self.uid = uid
        self.name = name


class CrossVersionObjectReference(KubernetesBaseObject):
    """
    :param api_version:API version of the referent
    :type api_version: Optional[str]
    :param name:Name of the referent; More info: \
        http://kubernetes.io/docs/user-guide/identifiers#names
    :type name: Optional[str]
    """

    def __init__(self, api_version: Optional[str] = None, name: Optional[str] = None):
        super().__init__(api_version)
        self.name = name


class LocalObjectReference(HelmYaml):
    """
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: Optional[str]
    """

    def __init__(self, name: Optional[str] = None):
        self.name = name


class TypedLocalObjectReference(KubernetesBaseObject):
    """
    :param api_group:APIGroup is the group for the resource being referenced. If \
        APIGroup is not specified, the specified Kind must be in the core API group. \
        For any other third-party types, APIGroup is required.
    :type api_group: Optional[str]
    :param name:Name is the name of resource being referenced
    :type name: Optional[str]
    """

    def __init__(self, api_group: Optional[str] = None, name: Optional[str] = None):
        self.apiGroup = api_group
        self.name = name


class ObjectReference(KubernetesBaseObject):
    """
    :param field_path:If referring to a piece of an object instead of an entire \
        object, this string should contain a valid JSON/Go field access statement, \
        such as desiredState.manifest.containers[2]. For example, if the object \
        reference is to a container within a pod, this would take on a value like: \
        "spec.containers{name}" (where "name" refers to the name of the container that \
        triggered the event) or if no container name is specified "spec.containers[2]" \
        (container with index 2 in this pod). This syntax is chosen only to have some \
        well-defined way of referencing a part of an object.
    :type field_path: str
    :param resource_version:Specific resourceVersion to which this reference is made, \
        if any. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency  # noqa
    :type resource_version: str
    :param uid:UID of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids
    :type uid: str
    :param api_version:API version of the referent.
    :type api_version: Optional[str]
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: Optional[str]
    :param namespace:Namespace of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
    :type namespace: Optional[str]
    """

    def __init__(
        self,
        field_path: str,
        resource_version: str,
        uid: str,
        api_version: Optional[str] = None,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.fieldPath = field_path
        self.resourceVersion = resource_version
        self.uid = uid
        self.name = name
        self.namespace = namespace
