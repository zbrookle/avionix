from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.topology import TopologySelectorTerm


class StorageClass(KubernetesBaseObject):
    """
    :param allow_volume_expansion:AllowVolumeExpansion shows whether the storage class \
        allow volume expand
    :type allow_volume_expansion: bool
    :param allowed_topologies:Restrict the node topologies where volumes can be \
        dynamically provisioned. Each volume plugin defines its own supported topology \
        specifications. An empty TopologySelectorTerm list means there is no topology \
        restriction. This field is only honored by servers that enable the \
        VolumeScheduling feature.
    :type allowed_topologies: List[TopologySelectorTerm]
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param mount_options:Dynamically provisioned PersistentVolumes of this storage \
        class are created with these mountOptions, e.g. ["ro", "soft"]. Not validated \
        - mount of the PVs will simply fail if one is invalid.
    :type mount_options: List[str]
    :param parameters:Parameters holds the parameters for the provisioner that should \
        create volumes of this storage class.
    :type parameters: dict
    :param provisioner:Provisioner indicates the type of the provisioner.
    :type provisioner: str
    :param volume_binding_mode:VolumeBindingMode indicates how PersistentVolumeClaims \
        should be provisioned and bound.  When unset, VolumeBindingImmediate is used. \
        This field is only honored by servers that enable the VolumeScheduling \
        feature.
    :type volume_binding_mode: str
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    :param reclaim_policy:Dynamically provisioned PersistentVolumes of this storage \
        class are created with this reclaimPolicy. Defaults to Delete.
    :type reclaim_policy: Optional[str]
    """

    def __init__(
        self,
        allow_volume_expansion: bool,
        allowed_topologies: List[TopologySelectorTerm],
        metadata: ObjectMeta,
        mount_options: List[str],
        parameters: dict,
        provisioner: str,
        volume_binding_mode: str,
        api_version: Optional[str] = None,
        reclaim_policy: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.allowVolumeExpansion = allow_volume_expansion
        self.allowedTopologies = allowed_topologies
        self.metadata = metadata
        self.mountOptions = mount_options
        self.parameters = parameters
        self.provisioner = provisioner
        self.volumeBindingMode = volume_binding_mode
        self.reclaimPolicy = reclaim_policy


class StorageClassList(KubernetesBaseObject):
    """
    :param items:Items is the list of StorageClasses
    :type items: List[StorageClass]
    :param metadata:Standard list metadata More info: \
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
        items: List[StorageClass],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
