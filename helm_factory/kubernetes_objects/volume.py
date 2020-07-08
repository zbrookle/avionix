from datetime import time
from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.config_map import ConfigMapProjection
from helm_factory.kubernetes_objects.general import KeyToPath, ResourceRequirements
from helm_factory.kubernetes_objects.metadata import ListMeta, ObjectMeta
from helm_factory.kubernetes_objects.node import VolumeNodeAffinity
from helm_factory.kubernetes_objects.reference import (
    LocalObjectReference,
    ObjectReference,
    TypedLocalObjectReference,
)
from helm_factory.kubernetes_objects.secret import SecretProjection, SecretReference
from helm_factory.kubernetes_objects.selector import (
    LabelSelector,
    ObjectFieldSelector,
    ResourceFieldSelector,
)
from helm_factory.kubernetes_objects.token import ServiceAccountTokenProjection
from helm_factory.yaml.yaml_handling import HelmYaml


class VsphereVirtualDiskVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :param storage_policy_id: Storage Policy Based Management (SPBM) profile ID \
        associated with the StoragePolicyName.
    :param storage_policy_name: Storage Policy Based Management (SPBM) profile name.
    :param volume_path: Path that identifies vSphere volume vmdk
    """

    def __init__(
        self,
        fs_type: str,
        storage_policy_id: str,
        storage_policy_name: str,
        volume_path: str,
    ):
        self.fsType = fs_type
        self.storagePolicyID = storage_policy_id
        self.storagePolicyName = storage_policy_name
        self.volumePath = volume_path


class GlusterfsVolumeSource(HelmYaml):
    """
    :param endpoints: EndpointsName is the endpoint name that details Glusterfs \
        topology. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :param path: Path is the Glusterfs volume path. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :param read_only: ReadOnly here will force the Glusterfs volume to be mounted with \
        read-only permissions. Defaults to false. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    """

    def __init__(self, endpoints: str, path: str, read_only: Optional[bool] = None):
        self.endpoints = endpoints
        self.path = path
        self.readOnly = read_only


class PersistentVolumeClaimSpec(HelmYaml):
    """
    :param access_modes: AccessModes contains the desired access modes the volume \
        should have. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes-1
    :param data_source: This field can be used to specify either: * An existing \
        VolumeSnapshot object (snapshot.storage.k8s.io/VolumeSnapshot - Beta) * An \
        existing PVC (PersistentVolumeClaim) * An existing custom resource/object that \
        implements data population (Alpha) In order to use VolumeSnapshot object \
        types, the appropriate feature gate must be enabled (VolumeSnapshotDataSource \
        or AnyVolumeDataSource) If the provisioner or an external controller can \
        support the specified data source, it will create a new volume based on the \
        contents of the specified data source. If the specified data source is not \
        supported, the volume will not be created and the failure will be reported as \
        an event. In the future, we plan to support more data source types and the \
        behavior of the provisioner may change.
    :param storage_class_name: Name of the StorageClass required by the claim. More \
        info: https://kubernetes.io/docs/concepts/storage/persistent-volumes#class-1
    :param volume_mode: volumeMode defines what type of volume is required by the \
        claim. Value of Filesystem is implied when not included in claim spec.
    :param volume_name: VolumeName is the binding reference to the PersistentVolume \
        backing this claim.
    :param resources: Resources represents the minimum resources the volume should \
        have. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#resources
    :param selector: A label query over volumes to consider for binding.
    """

    def __init__(
        self,
        access_modes: List[str],
        data_source: TypedLocalObjectReference,
        storage_class_name: str,
        volume_mode: str,
        volume_name: str,
        resources: Optional[ResourceRequirements] = None,
        selector: Optional[LabelSelector] = None,
    ):
        self.accessModes = access_modes
        self.dataSource = data_source
        self.storageClassName = storage_class_name
        self.volumeMode = volume_mode
        self.volumeName = volume_name
        self.resources = resources
        self.selector = selector


class PersistentVolumeClaimCondition(HelmYaml):
    """
    :param last_probe_time: Last time we probed the condition.
    :param last_transition_time: Last time the condition transitioned from one status \
        to another.
    :param message: Human-readable message indicating details about last transition.
    :param reason: Unique, this should be a short, machine understandable string that \
        gives the reason for condition's last transition. If it reports \
        "ResizeStarted" that means the underlying persistent volume is being resized.
    :param type: None
    """

    def __init__(
        self,
        last_probe_time: time,
        last_transition_time: time,
        message: str,
        reason: str,
        type: str,
    ):
        self.lastProbeTime = last_probe_time
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class PersistentVolumeClaim(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: Spec defines the desired characteristics of a volume requested by a \
        pod author. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims  # noqa
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: PersistentVolumeClaimSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class VolumeDevice(HelmYaml):
    """
    :param device_path: devicePath is the path inside of the container that the device \
        will be mapped to.
    :param name: name must match the name of a persistentVolumeClaim in the pod
    """

    def __init__(self, device_path: str, name: Optional[str] = None):
        self.devicePath = device_path
        self.name = name


class VolumeMount(HelmYaml):
    """
    :param mount_path: Path within the container at which the volume should be \
        mounted.  Must not contain ':'.
    :param mount_propagation: mountPropagation determines how mounts are propagated \
        from the host to container and the other way around. When not set, \
        MountPropagationNone is used. This field is beta in 1.10.
    :param name: This must match the Name of a Volume.
    :param read_only: Mounted read-only if true, read-write otherwise (false or \
        unspecified). Defaults to false.
    :param sub_path: Path within the volume from which the container's volume should \
        be mounted. Defaults to "" (volume's root).
    :param sub_path_expr: Expanded path within the volume from which the container's \
        volume should be mounted. Behaves similarly to SubPath but environment \
        variable references $(VAR_NAME) are expanded using the container's \
        environment. Defaults to "" (volume's root). SubPathExpr and SubPath are \
        mutually exclusive.
    """

    def __init__(
        self,
        mount_path: str,
        mount_propagation: str,
        name: Optional[str] = None,
        read_only: Optional[bool] = None,
        sub_path: Optional[str] = None,
        sub_path_expr: Optional[str] = None,
    ):
        self.mountPath = mount_path
        self.mountPropagation = mount_propagation
        self.name = name
        self.readOnly = read_only
        self.subPath = sub_path
        self.subPathExpr = sub_path_expr


class DownwardAPIVolumeFile(HelmYaml):
    """
    :param field_ref: Required: Selects a field of the pod: only annotations, labels, \
        name and namespace are supported.
    :param path: Required: Path is  the relative path name of the file to be created. \
        Must not be absolute or contain the '..' path. Must be utf-8 encoded. The \
        first item of the relative path must not start with '..'
    :param resource_field_ref: Selects a resource of the container: only resources \
        limits and requests (limits.cpu, limits.memory, requests.cpu and \
        requests.memory) are currently supported.
    :param mode: Optional: mode bits to use on this file, must be a value between 0 \
        and 0777. If not specified, the volume defaultMode will be used. This might be \
        in conflict with other options that affect the file mode, like fsGroup, and \
        the result can be other mode bits set.
    """

    def __init__(
        self,
        field_ref: ObjectFieldSelector,
        path: str,
        resource_field_ref: ResourceFieldSelector,
        mode: Optional[int] = None,
    ):
        self.fieldRef = field_ref
        self.path = path
        self.resourceFieldRef = resource_field_ref
        self.mode = mode


class DownwardAPIVolumeSource(HelmYaml):
    """
    :param items: Items is a list of downward API volume file
    :param default_mode: Optional: mode bits to use on created files by default. Must \
        be a value between 0 and 0777. Defaults to 0644. Directories within the path \
        are not affected by this setting. This might be in conflict with other options \
        that affect the file mode, like fsGroup, and the result can be other mode bits \
        set.
    """

    def __init__(
        self, items: List[DownwardAPIVolumeFile], default_mode: Optional[int] = None
    ):
        self.items = items
        self.defaultMode = default_mode


class StorageOSVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :param volume_name: VolumeName is the human-readable name of the StorageOS volume. \
         Volume names are only unique within a namespace.
    :param volume_namespace: VolumeNamespace specifies the scope of the volume within \
        StorageOS.  If no namespace is specified then the Pod's namespace will be \
        used.  This allows the Kubernetes name scoping to be mirrored within StorageOS \
        for tighter integration. Set VolumeName to any name to override the default \
        behaviour. Set to "default" if you are not using namespaces within StorageOS. \
        Namespaces that do not pre-exist within StorageOS will be created.
    :param read_only: Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :param secret_ref: SecretRef specifies the secret to use for obtaining the \
        StorageOS API credentials.  If not specified, default values will be \
        attempted.
    """

    def __init__(
        self,
        fs_type: str,
        volume_name: str,
        volume_namespace: str,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
    ):
        self.fsType = fs_type
        self.volumeName = volume_name
        self.volumeNamespace = volume_namespace
        self.readOnly = read_only
        self.secretRef = secret_ref


class QuobyteVolumeSource(HelmYaml):
    """
    :param registry: Registry represents a single or multiple Quobyte Registry \
        services specified as a string as host:port pair (multiple entries are \
        separated with commas) which acts as the central registry for volumes
    :param tenant: Tenant owning the given Quobyte volume in the Backend Used with \
        dynamically provisioned Quobyte volumes, value is set by the plugin
    :param volume: Volume is a string that references an already created Quobyte \
        volume by name.
    :param group: Group to map volume access to Default is no group
    :param read_only: ReadOnly here will force the Quobyte volume to be mounted with \
        read-only permissions. Defaults to false.
    :param user: User to map volume access to Defaults to serivceaccount user
    """

    def __init__(
        self,
        registry: str,
        tenant: str,
        volume: str,
        group: Optional[str] = None,
        read_only: Optional[bool] = None,
        user: Optional[str] = None,
    ):
        self.registry = registry
        self.tenant = tenant
        self.volume = volume
        self.group = group
        self.readOnly = read_only
        self.user = user


class CinderVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly \
        inferred to be "ext4" if unspecified. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :param volume_id: volume id used to identify the volume in cinder. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :param read_only: Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :param secret_ref: Optional: points to a secret object containing parameters used \
        to connect to OpenStack.
    """

    def __init__(
        self,
        fs_type: str,
        volume_id: str,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
    ):
        self.fsType = fs_type
        self.volumeID = volume_id
        self.readOnly = read_only
        self.secretRef = secret_ref


class PortworxVolumeSource(HelmYaml):
    """
    :param fs_type: FSType represents the filesystem type to mount Must be a \
        filesystem type supported by the host operating system. Ex. "ext4", "xfs". \
        Implicitly inferred to be "ext4" if unspecified.
    :param volume_id: VolumeID uniquely identifies a Portworx volume
    :param read_only: Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    """

    def __init__(self, fs_type: str, volume_id: str, read_only: Optional[bool] = None):
        self.fsType = fs_type
        self.volumeID = volume_id
        self.readOnly = read_only


class GCEPersistentDiskVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :param pd_name: Unique name of the PD resource in GCE. Used to identify the disk \
        in GCE. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :param partition: The partition in the volume that you want to mount. If omitted, \
        the default is to mount by volume name. Examples: For volume /dev/sda1, you \
        specify the partition as "1". Similarly, the volume partition for /dev/sda is \
        "0" (or you can leave the property empty). More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :param read_only: ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    """

    def __init__(
        self,
        fs_type: str,
        pd_name: str,
        partition: Optional[int] = None,
        read_only: Optional[bool] = None,
    ):
        self.fsType = fs_type
        self.pdName = pd_name
        self.partition = partition
        self.readOnly = read_only


class ISCSIVolumeSource(HelmYaml):
    """
    :param chap_auth_discovery: whether support iSCSI Discovery CHAP authentication
    :param chap_auth_session: whether support iSCSI Session CHAP authentication
    :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi
    :param initiator_name: Custom iSCSI Initiator Name. If initiatorName is specified \
        with iscsiInterface simultaneously, new iSCSI interface <target \
        portal>:<volume name> will be created for the connection.
    :param iqn: Target iSCSI Qualified Name.
    :param lun: iSCSI Target Lun number.
    :param portals: iSCSI Target Portal List. The portal is either an IP or \
        ip_addr:port if the port is other than default (typically TCP ports 860 and \
        3260).
    :param secret_ref: CHAP Secret for iSCSI target and initiator authentication
    :param target_portal: iSCSI Target Portal. The Portal is either an IP or \
        ip_addr:port if the port is other than default (typically TCP ports 860 and \
        3260).
    :param iscsi_interface: iSCSI Interface Name that uses an iSCSI transport. \
        Defaults to 'default' (tcp).
    :param read_only: ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false.
    """

    def __init__(
        self,
        chap_auth_discovery: bool,
        chap_auth_session: bool,
        fs_type: str,
        initiator_name: str,
        iqn: str,
        lun: int,
        portals: List[str],
        secret_ref: LocalObjectReference,
        target_portal: str,
        iscsi_interface: Optional[str] = None,
        read_only: Optional[bool] = None,
    ):
        self.chapAuthDiscovery = chap_auth_discovery
        self.chapAuthSession = chap_auth_session
        self.fsType = fs_type
        self.initiatorName = initiator_name
        self.iqn = iqn
        self.lun = lun
        self.portals = portals
        self.secretRef = secret_ref
        self.targetPortal = target_portal
        self.iscsiInterface = iscsi_interface
        self.readOnly = read_only


class NFSVolumeSource(HelmYaml):
    """
    :param path: Path that is exported by the NFS server. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#nfs
    :param server: Server is the hostname or IP address of the NFS server. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#nfs
    :param read_only: ReadOnly here will force the NFS export to be mounted with \
        read-only permissions. Defaults to false. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#nfs
    """

    def __init__(self, path: str, server: str, read_only: Optional[bool] = None):
        self.path = path
        self.server = server
        self.readOnly = read_only


class CSIVolumeSource(HelmYaml):
    """
    :param driver: Driver is the name of the CSI driver that handles this volume. \
        Consult with your admin for the correct name as registered in the cluster.
    :param fs_type: Filesystem type to mount. Ex. "ext4", "xfs", "ntfs". If not \
        provided, the empty value is passed to the associated CSI driver which will \
        determine the default filesystem to apply.
    :param volume_attributes: VolumeAttributes stores driver-specific properties that \
        are passed to the CSI driver. Consult your driver's documentation for \
        supported values.
    :param node_publish_secret_ref: NodePublishSecretRef is a reference to the secret \
        object containing sensitive information to pass to the CSI driver to complete \
        the CSI NodePublishVolume and NodeUnpublishVolume calls. This field is \
        optional, and  may be empty if no secret is required. If the secret object \
        contains more than one secret, all secret references are passed.
    :param read_only: Specifies a read-only configuration for the volume. Defaults to \
        false (read/write).
    """

    def __init__(
        self,
        driver: str,
        fs_type: str,
        volume_attributes: dict,
        node_publish_secret_ref: Optional[LocalObjectReference] = None,
        read_only: Optional[bool] = None,
    ):
        self.driver = driver
        self.fsType = fs_type
        self.volumeAttributes = volume_attributes
        self.nodePublishSecretRef = node_publish_secret_ref
        self.readOnly = read_only


class GitRepoVolumeSource(HelmYaml):
    """
    :param repository: Repository URL
    :param revision: Commit hash for the specified revision.
    :param directory: Target directory name. Must not contain or start with '..'.  If \
        '.' is supplied, the volume directory will be the git repository.  Otherwise, \
        if specified, the volume will contain the git repository in the subdirectory \
        with the given name.
    """

    def __init__(self, repository: str, revision: str, directory: Optional[str] = None):
        self.repository = repository
        self.revision = revision
        self.directory = directory


class EmptyDirVolumeSource(HelmYaml):
    """
    :param medium: What type of storage medium should back this directory. The default \
        is "" which means to use the node's default medium. Must be an empty string \
        (default) or Memory. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#emptydir
    :param size_limit: Total amount of local storage required for this EmptyDir \
        volume. The size limit is also applicable for memory medium. The maximum usage \
        on memory medium EmptyDir would be the minimum value between the SizeLimit \
        specified here and the sum of memory limits of all containers in a pod. The \
        default is nil which means that the limit is undefined. More info: \
        http://kubernetes.io/docs/user-guide/volumes#emptydir
    """

    def __init__(self, medium: Optional[str] = None, size_limit: Optional[str] = None):
        self.medium = medium
        self.sizeLimit = size_limit


class PersistentVolumeClaimVolumeSource(HelmYaml):
    """
    :param claim_name: ClaimName is the name of a PersistentVolumeClaim in the same \
        namespace as the pod using this volume. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims  # noqa
    :param read_only: Will force the ReadOnly setting in VolumeMounts. Default false.
    """

    def __init__(self, claim_name: str, read_only: bool):
        self.claimName = claim_name
        self.readOnly = read_only


class FlockerVolumeSource(HelmYaml):
    """
    :param dataset_name: Name of the dataset stored as metadata -> name on the dataset \
        for Flocker should be considered as deprecated
    :param dataset_uuid: UUID of the dataset. This is unique identifier of a Flocker \
        dataset
    """

    def __init__(self, dataset_name: str, dataset_uuid: str):
        self.datasetName = dataset_name
        self.datasetUUID = dataset_uuid


class DownwardAPIProjection(HelmYaml):
    """
    :param items: Items is a list of DownwardAPIVolume file
    """

    def __init__(self, items: List[DownwardAPIVolumeFile]):
        self.items = items


class VolumeProjection(HelmYaml):
    """
    :param config_map: information about the configMap data to project
    :param downward_api: information about the downwardAPI data to project
    :param secret: information about the secret data to project
    :param service_account_token: information about the serviceAccountToken data to \
        project
    """

    def __init__(
        self,
        config_map: ConfigMapProjection,
        downward_api: DownwardAPIProjection,
        secret: SecretProjection,
        service_account_token: ServiceAccountTokenProjection,
    ):
        self.configMap = config_map
        self.downwardAPI = downward_api
        self.secret = secret
        self.serviceAccountToken = service_account_token


class ProjectedVolumeSource(HelmYaml):
    """
    :param default_mode: Mode bits to use on created files by default. Must be a value \
        between 0 and 0777. Directories within the path are not affected by this \
        setting. This might be in conflict with other options that affect the file \
        mode, like fsGroup, and the result can be other mode bits set.
    :param sources: list of volume projections
    """

    def __init__(self, default_mode: int, sources: List[VolumeProjection]):
        self.defaultMode = default_mode
        self.sources = sources


class FlexVolumeSource(HelmYaml):
    """
    :param driver: Driver is the name of the driver to use for this volume.
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". The default filesystem \
        depends on FlexVolume script.
    :param options: Optional: Extra command options if any.
    :param read_only: Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts.
    :param secret_ref: Optional: SecretRef is reference to the secret object \
        containing sensitive information to pass to the plugin scripts. This may be \
        empty if no secret object is specified. If the secret object contains more \
        than one secret, all secrets are passed to the plugin scripts.
    """

    def __init__(
        self,
        driver: str,
        fs_type: str,
        options: Optional[dict] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
    ):
        self.driver = driver
        self.fsType = fs_type
        self.options = options
        self.readOnly = read_only
        self.secretRef = secret_ref


class PhotonPersistentDiskVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :param pd_id: ID that identifies Photon Controller persistent disk
    """

    def __init__(self, fs_type: str, pd_id: str):
        self.fsType = fs_type
        self.pdID = pd_id


class CephFSVolumeSource(HelmYaml):
    """
    :param monitors: Required: Monitors is a collection of Ceph monitors More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :param path: Optional: Used as the mounted root, rather than the full Ceph tree, \
        default is /
    :param read_only: Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts. More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :param secret_file: Optional: SecretFile is the path to key ring for User, default \
        is /etc/ceph/user.secret More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :param secret_ref: Optional: SecretRef is reference to the authentication secret \
        for User, default is empty. More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :param user: Optional: User is the rados user name, default is admin More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    """

    def __init__(
        self,
        monitors: List[str],
        path: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_file: Optional[str] = None,
        secret_ref: Optional[LocalObjectReference] = None,
        user: Optional[str] = None,
    ):
        self.monitors = monitors
        self.path = path
        self.readOnly = read_only
        self.secretFile = secret_file
        self.secretRef = secret_ref
        self.user = user


class AzureDiskVolumeSource(KubernetesBaseObject):
    """
    :param caching_mode: Host Caching mode: None, Read Only, Read Write.
    :param disk_name: The Name of the data disk in the blob storage
    :param disk_uri: The URI the data disk in the blob storage
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :param read_only: Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    """

    def __init__(
        self,
        caching_mode: str,
        disk_name: str,
        disk_uri: str,
        fs_type: str,
        read_only: Optional[bool] = None,
    ):
        self.cachingMode = caching_mode
        self.diskName = disk_name
        self.diskURI = disk_uri
        self.fsType = fs_type
        self.readOnly = read_only


class HostPathVolumeSource(HelmYaml):
    """
    :param path: Path of the directory on the host. If the path is a symlink, it will \
        follow the link to the real path. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#hostpath
    :param type: Type for HostPath Volume Defaults to "" More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#hostpath
    """

    def __init__(self, path: str, type: Optional[str] = None):
        self.path = path
        self.type = type


class ConfigMapVolumeSource(HelmYaml):
    """
    :param optional: Specify whether the ConfigMap or its keys must be defined
    :param default_mode: Optional: mode bits to use on created files by default. Must \
        be a value between 0 and 0777. Defaults to 0644. Directories within the path \
        are not affected by this setting. This might be in conflict with other options \
        that affect the file mode, like fsGroup, and the result can be other mode bits \
        set.
    :param items: If unspecified, each key-value pair in the Data field of the \
        referenced ConfigMap will be projected into the volume as a file whose name is \
        the key and content is the value. If specified, the listed keys will be \
        projected into the specified paths, and unlisted keys will not be present. If \
        a key is specified which is not present in the ConfigMap, the volume setup \
        will error unless it is marked optional. Paths must be relative and may not \
        contain the '..' path or start with '..'.
    :param name: Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    """

    def __init__(
        self,
        optional: bool,
        default_mode: Optional[int] = None,
        items: Optional[List[KeyToPath]] = None,
        name: Optional[str] = None,
    ):
        self.optional = optional
        self.defaultMode = default_mode
        self.items = items
        self.name = name


class FCVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :param lun: Optional: FC target lun number
    :param read_only: Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts.
    :param target_wwns: Optional: FC target worldwide names (WWNs)
    :param wwids: Optional: FC volume world wide identifiers (wwids) Either wwids or \
        combination of targetWWNs and lun must be set, but not both simultaneously.
    """

    def __init__(
        self,
        fs_type: str,
        lun: Optional[int] = None,
        read_only: Optional[bool] = None,
        target_wwns: Optional[List[str]] = None,
        wwids: Optional[List[str]] = None,
    ):
        self.fsType = fs_type
        self.lun = lun
        self.readOnly = read_only
        self.targetWWNs = target_wwns
        self.wwids = wwids


class ScaleIOVolumeSource(HelmYaml):
    """
    :param gateway: The host address of the ScaleIO API Gateway.
    :param protection_domain: The name of the ScaleIO Protection Domain for the \
        configured storage.
    :param ssl_enabled: Flag to enable/disable SSL communication with Gateway, default \
        false
    :param storage_pool: The ScaleIO Storage Pool associated with the protection \
        domain.
    :param system: The name of the storage system as configured in ScaleIO.
    :param volume_name: The name of a volume already created in the ScaleIO system \
        that is associated with this volume source.
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Default is "xfs".
    :param read_only: Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :param secret_ref: SecretRef references to the secret for ScaleIO user and other \
        sensitive information. If this is not provided, Login operation will fail.
    :param storage_mode: Indicates whether the storage for a volume should be \
        ThickProvisioned or ThinProvisioned. Default is ThinProvisioned.
    """

    def __init__(
        self,
        gateway: str,
        protection_domain: str,
        ssl_enabled: bool,
        storage_pool: str,
        system: str,
        volume_name: str,
        fs_type: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
        storage_mode: Optional[str] = None,
    ):
        self.gateway = gateway
        self.protectionDomain = protection_domain
        self.sslEnabled = ssl_enabled
        self.storagePool = storage_pool
        self.system = system
        self.volumeName = volume_name
        self.fsType = fs_type
        self.readOnly = read_only
        self.secretRef = secret_ref
        self.storageMode = storage_mode


class AzureFileVolumeSource(HelmYaml):
    """
    :param secret_name: the name of secret that contains Azure Storage Account Name \
        and Key
    :param share_name: Share Name
    :param read_only: Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    """

    def __init__(
        self, secret_name: str, share_name: str, read_only: Optional[bool] = None
    ):
        self.secretName = secret_name
        self.shareName = share_name
        self.readOnly = read_only


class AWSElasticBlockStoreVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    :param volume_id: Unique ID of the persistent disk resource in AWS (Amazon EBS \
        volume). More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    :param partition: The partition in the volume that you want to mount. If omitted, \
        the default is to mount by volume name. Examples: For volume /dev/sda1, you \
        specify the partition as "1". Similarly, the volume partition for /dev/sda is \
        "0" (or you can leave the property empty).
    :param read_only: Specify "true" to force and set the ReadOnly property in \
        VolumeMounts to "true". If omitted, the default is "false". More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    """

    def __init__(
        self,
        fs_type: str,
        volume_id: str,
        partition: Optional[int] = None,
        read_only: Optional[bool] = None,
    ):
        self.fsType = fs_type
        self.volumeID = volume_id
        self.partition = partition
        self.readOnly = read_only


class SecretVolumeSource(HelmYaml):
    """
    :param optional: Specify whether the Secret or its keys must be defined
    :param secret_name: Name of the secret in the pod's namespace to use. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#secret
    :param default_mode: Optional: mode bits to use on created files by default. Must \
        be a value between 0 and 0777. Defaults to 0644. Directories within the path \
        are not affected by this setting. This might be in conflict with other options \
        that affect the file mode, like fsGroup, and the result can be other mode bits \
        set.
    :param items: If unspecified, each key-value pair in the Data field of the \
        referenced Secret will be projected into the volume as a file whose name is \
        the key and content is the value. If specified, the listed keys will be \
        projected into the specified paths, and unlisted keys will not be present. If \
        a key is specified which is not present in the Secret, the volume setup will \
        error unless it is marked optional. Paths must be relative and may not contain \
        the '..' path or start with '..'.
    """

    def __init__(
        self,
        optional: bool,
        secret_name: str,
        default_mode: Optional[int] = None,
        items: Optional[List[KeyToPath]] = None,
    ):
        self.optional = optional
        self.secretName = secret_name
        self.defaultMode = default_mode
        self.items = items


class RBDVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#rbd
    :param image: The rados image name. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param monitors: A collection of Ceph monitors. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param keyring: Keyring is the path to key ring for RBDUser. Default is \
        /etc/ceph/keyring. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param pool: The rados pool name. Default is rbd. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param read_only: ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param secret_ref: SecretRef is name of the authentication secret for RBDUser. If \
        provided overrides keyring. Default is nil. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param user: The rados user name. Default is admin. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    """

    def __init__(
        self,
        fs_type: str,
        image: str,
        monitors: List[str],
        keyring: Optional[str] = None,
        pool: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[LocalObjectReference] = None,
        user: Optional[str] = None,
    ):
        self.fsType = fs_type
        self.image = image
        self.monitors = monitors
        self.keyring = keyring
        self.pool = pool
        self.readOnly = read_only
        self.secretRef = secret_ref
        self.user = user


class Volume(HelmYaml):
    """
    :param aws_elastic_block_store: AWSElasticBlockStore represents an AWS Disk \
        resource that is attached to a kubelet's host machine and then exposed to the \
        pod. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    :param azure_disk: AzureDisk represents an Azure Data Disk mount on the host and \
        bind mount to the pod.
    :param azure_file: AzureFile represents an Azure File Service mount on the host \
        and bind mount to the pod.
    :param cephfs: CephFS represents a Ceph FS mount on the host that shares a pod's \
        lifetime
    :param cinder: Cinder represents a cinder volume attached and mounted on kubelets \
        host machine. More info: https://examples.k8s.io/mysql-cinder-pd/README.md
    :param config_map: ConfigMap represents a configMap that should populate this \
        volume
    :param csi: CSI (Container Storage Interface) represents storage that is handled \
        by an external CSI driver (Alpha feature).
    :param downward_api: DownwardAPI represents downward API about the pod that should \
        populate this volume
    :param empty_dir: EmptyDir represents a temporary directory that shares a pod's \
        lifetime. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#emptydir
    :param fc: FC represents a Fibre Channel resource that is attached to a kubelet's \
        host machine and then exposed to the pod.
    :param flex_volume: FlexVolume represents a generic volume resource that is \
        provisioned/attached using an exec based plugin.
    :param flocker: Flocker represents a Flocker volume attached to a kubelet's host \
        machine. This depends on the Flocker control service being running
    :param gce_persistent_disk: GCEPersistentDisk represents a GCE Disk resource that \
        is attached to a kubelet's host machine and then exposed to the pod. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :param git_repo: GitRepo represents a git repository at a particular revision. \
        DEPRECATED: GitRepo is deprecated. To provision a container with a git repo, \
        mount an EmptyDir into an InitContainer that clones the repo using git, then \
        mount the EmptyDir into the Pod's container.
    :param glusterfs: Glusterfs represents a Glusterfs mount on the host that shares a \
        pod's lifetime. More info: https://examples.k8s.io/volumes/glusterfs/README.md
    :param host_path: HostPath represents a pre-existing file or directory on the host \
        machine that is directly exposed to the container. This is generally used for \
        system agents or other privileged things that are allowed to see the host \
        machine. Most containers will NOT need this. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#hostpath
    :param iscsi: ISCSI represents an ISCSI Disk resource that is attached to a \
        kubelet's host machine and then exposed to the pod. More info: \
        https://examples.k8s.io/volumes/iscsi/README.md
    :param nfs: NFS represents an NFS mount on the host that shares a pod's lifetime \
        More info: https://kubernetes.io/docs/concepts/storage/volumes#nfs
    :param persistent_volume_claim: PersistentVolumeClaimVolumeSource represents a \
        reference to a PersistentVolumeClaim in the same namespace. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims  # noqa
    :param photon_persistent_disk: PhotonPersistentDisk represents a PhotonController \
        persistent disk attached and mounted on kubelets host machine
    :param portworx_volume: PortworxVolume represents a portworx volume attached and \
        mounted on kubelets host machine
    :param projected: Items for all in one resources secrets, configmaps, and downward \
        API
    :param quobyte: Quobyte represents a Quobyte mount on the host that shares a pod's \
        lifetime
    :param rbd: RBD represents a Rados Block Device mount on the host that shares a \
        pod's lifetime. More info: https://examples.k8s.io/volumes/rbd/README.md
    :param scale_io: ScaleIO represents a ScaleIO persistent volume attached and \
        mounted on Kubernetes nodes.
    :param secret: Secret represents a secret that should populate this volume. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#secret
    :param storageos: StorageOS represents a StorageOS volume attached and mounted on \
        Kubernetes nodes.
    :param vsphere_volume: VsphereVolume represents a vSphere volume attached and \
        mounted on kubelets host machine
    :param name: Volume's name. Must be a DNS_LABEL and unique within the pod. More \
        info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    """

    def __init__(
        self,
        aws_elastic_block_store: AWSElasticBlockStoreVolumeSource,
        azure_disk: AzureDiskVolumeSource,
        azure_file: AzureFileVolumeSource,
        cephfs: CephFSVolumeSource,
        cinder: CinderVolumeSource,
        config_map: ConfigMapVolumeSource,
        csi: CSIVolumeSource,
        downward_api: DownwardAPIVolumeSource,
        empty_dir: EmptyDirVolumeSource,
        fc: FCVolumeSource,
        flex_volume: FlexVolumeSource,
        flocker: FlockerVolumeSource,
        gce_persistent_disk: GCEPersistentDiskVolumeSource,
        git_repo: GitRepoVolumeSource,
        glusterfs: GlusterfsVolumeSource,
        host_path: HostPathVolumeSource,
        iscsi: ISCSIVolumeSource,
        nfs: NFSVolumeSource,
        persistent_volume_claim: PersistentVolumeClaimVolumeSource,
        photon_persistent_disk: PhotonPersistentDiskVolumeSource,
        portworx_volume: PortworxVolumeSource,
        projected: ProjectedVolumeSource,
        quobyte: QuobyteVolumeSource,
        rbd: RBDVolumeSource,
        scale_io: ScaleIOVolumeSource,
        secret: SecretVolumeSource,
        storageos: StorageOSVolumeSource,
        vsphere_volume: VsphereVirtualDiskVolumeSource,
        name: Optional[str] = None,
    ):
        self.awsElasticBlockStore = aws_elastic_block_store
        self.azureDisk = azure_disk
        self.azureFile = azure_file
        self.cephfs = cephfs
        self.cinder = cinder
        self.configMap = config_map
        self.csi = csi
        self.downwardAPI = downward_api
        self.emptyDir = empty_dir
        self.fc = fc
        self.flexVolume = flex_volume
        self.flocker = flocker
        self.gcePersistentDisk = gce_persistent_disk
        self.gitRepo = git_repo
        self.glusterfs = glusterfs
        self.hostPath = host_path
        self.iscsi = iscsi
        self.nfs = nfs
        self.persistentVolumeClaim = persistent_volume_claim
        self.photonPersistentDisk = photon_persistent_disk
        self.portworxVolume = portworx_volume
        self.projected = projected
        self.quobyte = quobyte
        self.rbd = rbd
        self.scaleIO = scale_io
        self.secret = secret
        self.storageos = storageos
        self.vsphereVolume = vsphere_volume
        self.name = name


class AttachedVolume(HelmYaml):
    """
    :param device_path: DevicePath represents the device path where the volume should \
        be available
    :param name: Name of the attached volume
    """

    def __init__(self, device_path: str, name: Optional[str] = None):
        self.devicePath = device_path
        self.name = name


class ScaleIOPersistentVolumeSource(HelmYaml):
    """
    :param gateway: The host address of the ScaleIO API Gateway.
    :param protection_domain: The name of the ScaleIO Protection Domain for the \
        configured storage.
    :param ssl_enabled: Flag to enable/disable SSL communication with Gateway, default \
        false
    :param storage_pool: The ScaleIO Storage Pool associated with the protection \
        domain.
    :param system: The name of the storage system as configured in ScaleIO.
    :param volume_name: The name of a volume already created in the ScaleIO system \
        that is associated with this volume source.
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Default is "xfs"
    :param read_only: Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :param secret_ref: SecretRef references to the secret for ScaleIO user and other \
        sensitive information. If this is not provided, Login operation will fail.
    :param storage_mode: Indicates whether the storage for a volume should be \
        ThickProvisioned or ThinProvisioned. Default is ThinProvisioned.
    """

    def __init__(
        self,
        gateway: str,
        protection_domain: str,
        ssl_enabled: bool,
        storage_pool: str,
        system: str,
        volume_name: str,
        fs_type: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[SecretReference] = None,
        storage_mode: Optional[str] = None,
    ):
        self.gateway = gateway
        self.protectionDomain = protection_domain
        self.sslEnabled = ssl_enabled
        self.storagePool = storage_pool
        self.system = system
        self.volumeName = volume_name
        self.fsType = fs_type
        self.readOnly = read_only
        self.secretRef = secret_ref
        self.storageMode = storage_mode


class VolumeError(HelmYaml):
    """
    :param message: String detailing the error encountered during Attach or Detach \
        operation. This string may be logged, so it should not contain sensitive \
        information.
    :param time: Time the error was encountered.
    """

    def __init__(self, message: str, time: time):
        self.message = message
        self.time = time


class RBDPersistentVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#rbd
    :param image: The rados image name. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param monitors: A collection of Ceph monitors. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param keyring: Keyring is the path to key ring for RBDUser. Default is \
        /etc/ceph/keyring. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param pool: The rados pool name. Default is rbd. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param read_only: ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param secret_ref: SecretRef is name of the authentication secret for RBDUser. If \
        provided overrides keyring. Default is nil. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    :param user: The rados user name. Default is admin. More info: \
        https://examples.k8s.io/volumes/rbd/README.md#how-to-use-it
    """

    def __init__(
        self,
        fs_type: str,
        image: str,
        monitors: List[str],
        keyring: Optional[str] = None,
        pool: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[SecretReference] = None,
        user: Optional[str] = None,
    ):
        self.fsType = fs_type
        self.image = image
        self.monitors = monitors
        self.keyring = keyring
        self.pool = pool
        self.readOnly = read_only
        self.secretRef = secret_ref
        self.user = user


class StorageOSPersistentVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". Implicitly inferred to \
        be "ext4" if unspecified.
    :param volume_name: VolumeName is the human-readable name of the StorageOS volume. \
         Volume names are only unique within a namespace.
    :param volume_namespace: VolumeNamespace specifies the scope of the volume within \
        StorageOS.  If no namespace is specified then the Pod's namespace will be \
        used.  This allows the Kubernetes name scoping to be mirrored within StorageOS \
        for tighter integration. Set VolumeName to any name to override the default \
        behaviour. Set to "default" if you are not using namespaces within StorageOS. \
        Namespaces that do not pre-exist within StorageOS will be created.
    :param read_only: Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :param secret_ref: SecretRef specifies the secret to use for obtaining the \
        StorageOS API credentials.  If not specified, default values will be \
        attempted.
    """

    def __init__(
        self,
        fs_type: str,
        volume_name: str,
        volume_namespace: str,
        read_only: Optional[bool] = None,
        secret_ref: Optional[ObjectReference] = None,
    ):
        self.fsType = fs_type
        self.volumeName = volume_name
        self.volumeNamespace = volume_namespace
        self.readOnly = read_only
        self.secretRef = secret_ref


class AzureFilePersistentVolumeSource(HelmYaml):
    """
    :param secret_name: the name of secret that contains Azure Storage Account Name \
        and Key
    :param share_name: Share Name
    :param read_only: Defaults to false (read/write). ReadOnly here will force the \
        ReadOnly setting in VolumeMounts.
    :param secret_namespace: the namespace of the secret that contains Azure Storage \
        Account Name and Key default is the same as the Pod
    """

    def __init__(
        self,
        secret_name: str,
        share_name: str,
        read_only: Optional[bool] = None,
        secret_namespace: Optional[str] = None,
    ):
        self.secretName = secret_name
        self.shareName = share_name
        self.readOnly = read_only
        self.secretNamespace = secret_namespace


class VolumeNodeResources(HelmYaml):
    """
    :param count: Maximum number of unique volumes managed by the CSI driver that can \
        be used on a node. A volume that is both attached and mounted on a node is \
        considered to be used once, not twice. The same rule applies for a unique \
        volume that is shared among multiple pods on the same node. If this field is \
        not specified, then the supported number of volumes on this node is unbounded.
    """

    def __init__(self, count: int):
        self.count = count


class ISCSIPersistentVolumeSource(HelmYaml):
    """
    :param chap_auth_discovery: whether support iSCSI Discovery CHAP authentication
    :param chap_auth_session: whether support iSCSI Session CHAP authentication
    :param fs_type: Filesystem type of the volume that you want to mount. Tip: Ensure \
        that the filesystem type is supported by the host operating system. Examples: \
        "ext4", "xfs", "ntfs". Implicitly inferred to be "ext4" if unspecified. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#iscsi
    :param initiator_name: Custom iSCSI Initiator Name. If initiatorName is specified \
        with iscsiInterface simultaneously, new iSCSI interface <target \
        portal>:<volume name> will be created for the connection.
    :param iqn: Target iSCSI Qualified Name.
    :param lun: iSCSI Target Lun number.
    :param portals: iSCSI Target Portal List. The Portal is either an IP or \
        ip_addr:port if the port is other than default (typically TCP ports 860 and \
        3260).
    :param secret_ref: CHAP Secret for iSCSI target and initiator authentication
    :param target_portal: iSCSI Target Portal. The Portal is either an IP or \
        ip_addr:port if the port is other than default (typically TCP ports 860 and \
        3260).
    :param iscsi_interface: iSCSI Interface Name that uses an iSCSI transport. \
        Defaults to 'default' (tcp).
    :param read_only: ReadOnly here will force the ReadOnly setting in VolumeMounts. \
        Defaults to false.
    """

    def __init__(
        self,
        chap_auth_discovery: bool,
        chap_auth_session: bool,
        fs_type: str,
        initiator_name: str,
        iqn: str,
        lun: int,
        portals: List[str],
        secret_ref: SecretReference,
        target_portal: str,
        iscsi_interface: Optional[str] = None,
        read_only: Optional[bool] = None,
    ):
        self.chapAuthDiscovery = chap_auth_discovery
        self.chapAuthSession = chap_auth_session
        self.fsType = fs_type
        self.initiatorName = initiator_name
        self.iqn = iqn
        self.lun = lun
        self.portals = portals
        self.secretRef = secret_ref
        self.targetPortal = target_portal
        self.iscsiInterface = iscsi_interface
        self.readOnly = read_only


class LocalVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type to mount. It applies only when the Path is a block \
        device. Must be a filesystem type supported by the host operating system. Ex. \
        "ext4", "xfs", "ntfs". The default value is to auto-select a fileystem if \
        unspecified.
    :param path: The full path to the volume on the node. It can be either a directory \
        or block device (disk, partition, ...).
    """

    def __init__(self, fs_type: str, path: str):
        self.fsType = fs_type
        self.path = path


class CinderPersistentVolumeSource(HelmYaml):
    """
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Examples: "ext4", "xfs", "ntfs". Implicitly \
        inferred to be "ext4" if unspecified. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :param volume_id: volume id used to identify the volume in cinder. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :param read_only: Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts. More info: \
        https://examples.k8s.io/mysql-cinder-pd/README.md
    :param secret_ref: Optional: points to a secret object containing parameters used \
        to connect to OpenStack.
    """

    def __init__(
        self,
        fs_type: str,
        volume_id: str,
        read_only: Optional[bool] = None,
        secret_ref: Optional[SecretReference] = None,
    ):
        self.fsType = fs_type
        self.volumeID = volume_id
        self.readOnly = read_only
        self.secretRef = secret_ref


class FlexPersistentVolumeSource(HelmYaml):
    """
    :param driver: Driver is the name of the driver to use for this volume.
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs". The default filesystem \
        depends on FlexVolume script.
    :param options: Optional: Extra command options if any.
    :param read_only: Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts.
    :param secret_ref: Optional: SecretRef is reference to the secret object \
        containing sensitive information to pass to the plugin scripts. This may be \
        empty if no secret object is specified. If the secret object contains more \
        than one secret, all secrets are passed to the plugin scripts.
    """

    def __init__(
        self,
        driver: str,
        fs_type: str,
        options: Optional[dict] = None,
        read_only: Optional[bool] = None,
        secret_ref: Optional[SecretReference] = None,
    ):
        self.driver = driver
        self.fsType = fs_type
        self.options = options
        self.readOnly = read_only
        self.secretRef = secret_ref


class CSIPersistentVolumeSource(HelmYaml):
    """
    :param driver: Driver is the name of the driver to use for this volume. Required.
    :param fs_type: Filesystem type to mount. Must be a filesystem type supported by \
        the host operating system. Ex. "ext4", "xfs", "ntfs".
    :param volume_attributes: Attributes of the volume to publish.
    :param volume_handle: VolumeHandle is the unique volume name returned by the CSI \
        volume plugin’s CreateVolume to refer to the volume on all subsequent calls. \
        Required.
    :param controller_expand_secret_ref: ControllerExpandSecretRef is a reference to \
        the secret object containing sensitive information to pass to the CSI driver \
        to complete the CSI ControllerExpandVolume call. This is an alpha field and \
        requires enabling ExpandCSIVolumes feature gate. This field is optional, and \
        may be empty if no secret is required. If the secret object contains more than \
        one secret, all secrets are passed.
    :param controller_publish_secret_ref: ControllerPublishSecretRef is a reference to \
        the secret object containing sensitive information to pass to the CSI driver \
        to complete the CSI ControllerPublishVolume and ControllerUnpublishVolume \
        calls. This field is optional, and may be empty if no secret is required. If \
        the secret object contains more than one secret, all secrets are passed.
    :param node_publish_secret_ref: NodePublishSecretRef is a reference to the secret \
        object containing sensitive information to pass to the CSI driver to complete \
        the CSI NodePublishVolume and NodeUnpublishVolume calls. This field is \
        optional, and may be empty if no secret is required. If the secret object \
        contains more than one secret, all secrets are passed.
    :param node_stage_secret_ref: NodeStageSecretRef is a reference to the secret \
        object containing sensitive information to pass to the CSI driver to complete \
        the CSI NodeStageVolume and NodeStageVolume and NodeUnstageVolume calls. This \
        field is optional, and may be empty if no secret is required. If the secret \
        object contains more than one secret, all secrets are passed.
    :param read_only: Optional: The value to pass to ControllerPublishVolumeRequest. \
        Defaults to false (read/write).
    """

    def __init__(
        self,
        driver: str,
        fs_type: str,
        volume_attributes: dict,
        volume_handle: str,
        controller_expand_secret_ref: Optional[SecretReference] = None,
        controller_publish_secret_ref: Optional[SecretReference] = None,
        node_publish_secret_ref: Optional[SecretReference] = None,
        node_stage_secret_ref: Optional[SecretReference] = None,
        read_only: Optional[bool] = None,
    ):
        self.driver = driver
        self.fsType = fs_type
        self.volumeAttributes = volume_attributes
        self.volumeHandle = volume_handle
        self.controllerExpandSecretRef = controller_expand_secret_ref
        self.controllerPublishSecretRef = controller_publish_secret_ref
        self.nodePublishSecretRef = node_publish_secret_ref
        self.nodeStageSecretRef = node_stage_secret_ref
        self.readOnly = read_only


class GlusterfsPersistentVolumeSource(HelmYaml):
    """
    :param endpoints: EndpointsName is the endpoint name that details Glusterfs \
        topology. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :param path: Path is the Glusterfs volume path. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :param endpoints_namespace: EndpointsNamespace is the namespace that contains \
        Glusterfs endpoint. If this field is empty, the EndpointNamespace defaults to \
        the same namespace as the bound PVC. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    :param read_only: ReadOnly here will force the Glusterfs volume to be mounted with \
        read-only permissions. Defaults to false. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md#create-a-pod
    """

    def __init__(
        self,
        endpoints: str,
        path: str,
        endpoints_namespace: Optional[str] = None,
        read_only: Optional[bool] = None,
    ):
        self.endpoints = endpoints
        self.path = path
        self.endpointsNamespace = endpoints_namespace
        self.readOnly = read_only


class CephFSPersistentVolumeSource(HelmYaml):
    """
    :param monitors: Required: Monitors is a collection of Ceph monitors More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :param path: Optional: Used as the mounted root, rather than the full Ceph tree, \
        default is /
    :param read_only: Optional: Defaults to false (read/write). ReadOnly here will \
        force the ReadOnly setting in VolumeMounts. More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :param secret_file: Optional: SecretFile is the path to key ring for User, default \
        is /etc/ceph/user.secret More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :param secret_ref: Optional: SecretRef is reference to the authentication secret \
        for User, default is empty. More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    :param user: Optional: User is the rados user name, default is admin More info: \
        https://examples.k8s.io/volumes/cephfs/README.md#how-to-use-it
    """

    def __init__(
        self,
        monitors: List[str],
        path: Optional[str] = None,
        read_only: Optional[bool] = None,
        secret_file: Optional[str] = None,
        secret_ref: Optional[SecretReference] = None,
        user: Optional[str] = None,
    ):
        self.monitors = monitors
        self.path = path
        self.readOnly = read_only
        self.secretFile = secret_file
        self.secretRef = secret_ref
        self.user = user


class PersistentVolumeSpec(HelmYaml):
    """
    :param access_modes: AccessModes contains all ways the volume can be mounted. More \
        info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#access-modes
    :param aws_elastic_block_store: AWSElasticBlockStore represents an AWS Disk \
        resource that is attached to a kubelet's host machine and then exposed to the \
        pod. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#awselasticblockstore
    :param azure_disk: AzureDisk represents an Azure Data Disk mount on the host and \
        bind mount to the pod.
    :param azure_file: AzureFile represents an Azure File Service mount on the host \
        and bind mount to the pod.
    :param capacity: A description of the persistent volume's resources and capacity. \
        More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#capacity
    :param cephfs: CephFS represents a Ceph FS mount on the host that shares a pod's \
        lifetime
    :param cinder: Cinder represents a cinder volume attached and mounted on kubelets \
        host machine. More info: https://examples.k8s.io/mysql-cinder-pd/README.md
    :param claim_ref: ClaimRef is part of a bi-directional binding between \
        PersistentVolume and PersistentVolumeClaim. Expected to be non-nil when bound. \
        claim.VolumeName is the authoritative bind between PV and PVC. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#binding
    :param csi: CSI represents storage that is handled by an external CSI driver (Beta \
        feature).
    :param fc: FC represents a Fibre Channel resource that is attached to a kubelet's \
        host machine and then exposed to the pod.
    :param flex_volume: FlexVolume represents a generic volume resource that is \
        provisioned/attached using an exec based plugin.
    :param flocker: Flocker represents a Flocker volume attached to a kubelet's host \
        machine and exposed to the pod for its usage. This depends on the Flocker \
        control service being running
    :param gce_persistent_disk: GCEPersistentDisk represents a GCE Disk resource that \
        is attached to a kubelet's host machine and then exposed to the pod. \
        Provisioned by an admin. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#gcepersistentdisk
    :param glusterfs: Glusterfs represents a Glusterfs volume that is attached to a \
        host and exposed to the pod. Provisioned by an admin. More info: \
        https://examples.k8s.io/volumes/glusterfs/README.md
    :param host_path: HostPath represents a directory on the host. Provisioned by a \
        developer or tester. This is useful for single-node development and testing \
        only! On-host storage is not supported in any way and WILL NOT WORK in a \
        multi-node cluster. More info: \
        https://kubernetes.io/docs/concepts/storage/volumes#hostpath
    :param iscsi: ISCSI represents an ISCSI Disk resource that is attached to a \
        kubelet's host machine and then exposed to the pod. Provisioned by an admin.
    :param local: Local represents directly-attached storage with node affinity
    :param mount_options: A list of mount options, e.g. ["ro", "soft"]. Not validated \
        - mount will simply fail if one is invalid. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes/#mount-options
    :param nfs: NFS represents an NFS mount on the host. Provisioned by an admin. More \
        info: https://kubernetes.io/docs/concepts/storage/volumes#nfs
    :param node_affinity: NodeAffinity defines constraints that limit what nodes this \
        volume can be accessed from. This field influences the scheduling of pods that \
        use this volume.
    :param persistent_volume_reclaim_policy: What happens to a persistent volume when \
        released from its claim. Valid options are Retain (default for manually \
        created PersistentVolumes), Delete (default for dynamically provisioned \
        PersistentVolumes), and Recycle (deprecated). Recycle must be supported by the \
        volume plugin underlying this PersistentVolume. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#reclaiming
    :param photon_persistent_disk: PhotonPersistentDisk represents a PhotonController \
        persistent disk attached and mounted on kubelets host machine
    :param portworx_volume: PortworxVolume represents a portworx volume attached and \
        mounted on kubelets host machine
    :param quobyte: Quobyte represents a Quobyte mount on the host that shares a pod's \
        lifetime
    :param rbd: RBD represents a Rados Block Device mount on the host that shares a \
        pod's lifetime. More info: https://examples.k8s.io/volumes/rbd/README.md
    :param scale_io: ScaleIO represents a ScaleIO persistent volume attached and \
        mounted on Kubernetes nodes.
    :param storage_class_name: Name of StorageClass to which this persistent volume \
        belongs. Empty value means that this volume does not belong to any \
        StorageClass.
    :param storageos: StorageOS represents a StorageOS volume that is attached to the \
        kubelet's host machine and mounted into the pod More info: \
        https://examples.k8s.io/volumes/storageos/README.md
    :param volume_mode: volumeMode defines if a volume is intended to be used with a \
        formatted filesystem or to remain in raw block state. Value of Filesystem is \
        implied when not included in spec.
    :param vsphere_volume: VsphereVolume represents a vSphere volume attached and \
        mounted on kubelets host machine
    """

    def __init__(
        self,
        access_modes: List[str],
        aws_elastic_block_store: AWSElasticBlockStoreVolumeSource,
        azure_disk: AzureDiskVolumeSource,
        azure_file: AzureFilePersistentVolumeSource,
        capacity: dict,
        cephfs: CephFSPersistentVolumeSource,
        cinder: CinderPersistentVolumeSource,
        claim_ref: ObjectReference,
        csi: CSIPersistentVolumeSource,
        fc: FCVolumeSource,
        flex_volume: FlexPersistentVolumeSource,
        flocker: FlockerVolumeSource,
        gce_persistent_disk: GCEPersistentDiskVolumeSource,
        glusterfs: GlusterfsPersistentVolumeSource,
        host_path: HostPathVolumeSource,
        iscsi: ISCSIPersistentVolumeSource,
        local: LocalVolumeSource,
        mount_options: List[str],
        nfs: NFSVolumeSource,
        node_affinity: VolumeNodeAffinity,
        persistent_volume_reclaim_policy: str,
        photon_persistent_disk: PhotonPersistentDiskVolumeSource,
        portworx_volume: PortworxVolumeSource,
        quobyte: QuobyteVolumeSource,
        rbd: RBDPersistentVolumeSource,
        scale_io: ScaleIOPersistentVolumeSource,
        storage_class_name: str,
        storageos: StorageOSPersistentVolumeSource,
        volume_mode: str,
        vsphere_volume: VsphereVirtualDiskVolumeSource,
    ):
        self.accessModes = access_modes
        self.awsElasticBlockStore = aws_elastic_block_store
        self.azureDisk = azure_disk
        self.azureFile = azure_file
        self.capacity = capacity
        self.cephfs = cephfs
        self.cinder = cinder
        self.claimRef = claim_ref
        self.csi = csi
        self.fc = fc
        self.flexVolume = flex_volume
        self.flocker = flocker
        self.gcePersistentDisk = gce_persistent_disk
        self.glusterfs = glusterfs
        self.hostPath = host_path
        self.iscsi = iscsi
        self.local = local
        self.mountOptions = mount_options
        self.nfs = nfs
        self.nodeAffinity = node_affinity
        self.persistentVolumeReclaimPolicy = persistent_volume_reclaim_policy
        self.photonPersistentDisk = photon_persistent_disk
        self.portworxVolume = portworx_volume
        self.quobyte = quobyte
        self.rbd = rbd
        self.scaleIO = scale_io
        self.storageClassName = storage_class_name
        self.storageos = storageos
        self.volumeMode = volume_mode
        self.vsphereVolume = vsphere_volume


class PersistentVolume(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: Spec defines a specification of a persistent volume owned by the \
        cluster. Provisioned by an administrator. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistent-volumes  # noqa
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: PersistentVolumeSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class PersistentVolumeList(KubernetesBaseObject):
    """
    :param items: List of persistent volumes. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        items: List[PersistentVolume],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class VolumeAttachmentSource(HelmYaml):
    """
    :param inline_volume_spec: inlineVolumeSpec contains all the information necessary \
        to attach a persistent volume defined by a pod's inline VolumeSource. This \
        field is populated only for the CSIMigration feature. It contains translated \
        fields from a pod's inline VolumeSource to a PersistentVolumeSpec. This field \
        is alpha-level and is only honored by servers that enabled the CSIMigration \
        feature.
    :param persistent_volume_name: Name of the persistent volume to attach.
    """

    def __init__(
        self, inline_volume_spec: PersistentVolumeSpec, persistent_volume_name: str
    ):
        self.inlineVolumeSpec = inline_volume_spec
        self.persistentVolumeName = persistent_volume_name


class VolumeAttachmentSpec(HelmYaml):
    """
    :param attacher: Attacher indicates the name of the volume driver that MUST handle \
        this request. This is the name returned by GetPluginName().
    :param source: Source represents the volume that should be attached.
    :param node_name: The node that the volume should be attached to.
    """

    def __init__(
        self,
        attacher: str,
        source: VolumeAttachmentSource,
        node_name: Optional[str] = None,
    ):
        self.attacher = attacher
        self.source = source
        self.nodeName = node_name


class VolumeAttachment(KubernetesBaseObject):
    """
    :param metadata: Standard object metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: Specification of the desired attach/detach volume behavior. Populated \
        by the Kubernetes system.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: VolumeAttachmentSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class PersistentVolumeClaimList(KubernetesBaseObject):
    """
    :param items: A list of persistent volume claims. More info: \
        https://kubernetes.io/docs/concepts/storage/persistent-volumes#persistentvolumeclaims  # noqa
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        items: List[PersistentVolumeClaim],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class VolumeAttachmentList(KubernetesBaseObject):
    """
    :param items: Items is the list of VolumeAttachments
    :param metadata: Standard list metadata More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        items: List[VolumeAttachment],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
