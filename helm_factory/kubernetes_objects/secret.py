from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.general import KeyToPath
from helm_factory.kubernetes_objects.metadata import ListMeta, ObjectMeta
from helm_factory.yaml.yaml_handling import HelmYaml


class SecretReference(HelmYaml):
    """
    :param name: Name is unique within a namespace to reference a secret resource.
    :param namespace: Namespace defines the space within which the secret name must be \
        unique.
    """

    def __init__(self, name: Optional[str] = None, namespace: Optional[str] = None):
        self.name = name
        self.namespace = namespace


class SecretEnvSource(HelmYaml):
    """
    :param optional: Specify whether the Secret must be defined
    :param name: Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
    """

    def __init__(self, optional: bool, name: Optional[str] = None):
        self.optional = optional
        self.name = name


class SecretKeySelector(HelmYaml):
    """
    :param key: The key of the secret to select from.  Must be a valid secret key.
    :param optional: Specify whether the Secret or its key must be defined
    :param name: Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
    """

    def __init__(self, key: str, optional: bool, name: Optional[str] = None):
        self.key = key
        self.optional = optional
        self.name = name


class SecretProjection(HelmYaml):
    """
    :param optional: Specify whether the Secret or its key must be defined
    :param items: If unspecified, each key-value pair in the Data field of the \
        referenced Secret will be projected into the volume as a file whose name is \
        the key and content is the value. If specified, the listed keys will be \
        projected into the specified paths, and unlisted keys will not be present. If \
        a key is specified which is not present in the Secret, the volume setup will \
        error unless it is marked optional. Paths must be relative and may not contain \
        the '..' path or start with '..'.
    :param name: Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names
    """

    def __init__(
        self,
        optional: bool,
        items: Optional[List[KeyToPath]] = None,
        name: Optional[str] = None,
    ):
        self.optional = optional
        self.items = items
        self.name = name


class Secret(KubernetesBaseObject):
    """
    :param data: Data contains the secret data. Each key must consist of alphanumeric \
        characters, '-', '_' or '.'. The serialized form of the secret data is a \
        base64 encoded string, representing the arbitrary (possibly non-string) data \
        value here. Described in https://tools.ietf.org/html/rfc4648#section-4
    :param immutable: Immutable, if set to true, ensures that data stored in the \
        Secret cannot be updated (only object metadata can be modified). If not set to \
        true, the field can be modified at any time. Defaulted to nil. This is an \
        alpha field enabled by ImmutableEphemeralVolumes feature gate.
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    :param string_data: stringData allows specifying non-binary secret data in string \
        form. It is provided as a write-only convenience method. All keys and values \
        are merged into the data field on write, overwriting any existing values. It \
        is never output when reading from the API.
    :param type: Used to facilitate programmatic handling of secret data.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        data: dict,
        immutable: bool,
        metadata: ObjectMeta,
        string_data: dict,
        type: str,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.data = data
        self.immutable = immutable
        self.metadata = metadata
        self.stringData = string_data
        self.type = type


class SecretList(KubernetesBaseObject):
    """
    :param items: Items is a list of secret objects. More info: \
        https://kubernetes.io/docs/concepts/configuration/secret
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self, items: List[Secret], metadata: ListMeta, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
