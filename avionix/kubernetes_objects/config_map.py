from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.general import KeyToPath
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class ConfigMapProjection(HelmYaml):
    """
    :param optional:Specify whether the ConfigMap or its keys must be defined
    :type optional: bool
    :param items:If unspecified, each key-value pair in the Data field of the \
        referenced ConfigMap will be projected into the volume as a file whose name is \
        the key and content is the value. If specified, the listed keys will be \
        projected into the specified paths, and unlisted keys will not be present. If \
        a key is specified which is not present in the ConfigMap, the volume setup \
        will error unless it is marked optional. Paths must be relative and may not \
        contain the '..' path or start with '..'.
    :type items: Optional[List[KeyToPath]]
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: Optional[str]
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


class ConfigMapEnvSource(HelmYaml):
    """
    :param optional:Specify whether the ConfigMap must be defined
    :type optional: bool
    :param name:Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :type name: Optional[str]
    """

    def __init__(self, optional: bool, name: Optional[str] = None):
        self.optional = optional
        self.name = name


class ConfigMap(KubernetesBaseObject):
    """
    :param binary_data:BinaryData contains the binary data. Each key must consist of \
        alphanumeric characters, '-', '_' or '.'. BinaryData can contain byte \
        sequences that are not in the UTF-8 range. The keys stored in BinaryData must \
        not overlap with the ones in the Data field, this is enforced during \
        validation process. Using this field will require 1.10+ apiserver and kubelet.
    :type binary_data: dict
    :param data:Data contains the configuration data. Each key must consist of \
        alphanumeric characters, '-', '_' or '.'. Values with non-UTF-8 byte sequences \
        must use the BinaryData field. The keys stored in Data must not overlap with \
        the keys in the BinaryData field, this is enforced during validation process.
    :type data: dict
    :param immutable:Immutable, if set to true, ensures that data stored in the \
        ConfigMap cannot be updated (only object metadata can be modified). If not set \
        to true, the field can be modified at any time. Defaulted to nil. This is an \
        alpha field enabled by ImmutableEphemeralVolumes feature gate.
    :type immutable: bool
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        binary_data: dict,
        data: dict,
        immutable: bool,
        metadata: ObjectMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.binaryData = binary_data
        self.data = data
        self.immutable = immutable
        self.metadata = metadata


class ConfigMapList(KubernetesBaseObject):
    """
    :param items:Items is the list of ConfigMaps.
    :type items: List[ConfigMap]
    :param metadata:More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[ConfigMap],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
