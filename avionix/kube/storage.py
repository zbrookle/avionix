"""
Classes related to management of storage resources
"""

from typing import List, Optional

from avionix.kube.base_objects import Storage
from avionix.kube.core import PersistentVolumeSpec, TopologySelectorTerm
from avionix.kube.meta import ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


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


class CSINodeDriver(HelmYaml):
    """
    :param name: This is the name of the CSI driver that this object refers to. This \
        MUST be the same name returned by the CSI GetPluginName() call for that \
        driver.
    :param node_id: nodeID of the node from the driver point of view. This field \
        enables Kubernetes to communicate with storage systems that do not share the \
        same nomenclature for nodes. For example, Kubernetes may refer to a given node \
        as "node1", but the storage system may refer to the same node as "nodeA". When \
        Kubernetes issues a command to the storage system to attach a volume to a \
        specific node, it can use this field to refer to the node name using the ID \
        that the storage system will understand, e.g. "nodeA" instead of "node1". This \
        field is required.
    :param allocatable: allocatable represents the volume resources of a node that are \
        available for scheduling. This field is beta.
    :param topology_keys: topologyKeys is the list of keys supported by the driver. \
        When a driver is initialized on a cluster, it provides a set of topology keys \
        that it understands (e.g. "company.com/zone", "company.com/region"). When a \
        driver is initialized on a node, it provides the same topology keys along with \
        values. Kubelet will expose these topology keys as labels on its own node \
        object. When Kubernetes does topology aware provisioning, it can use this list \
        to determine which labels it should retrieve from the node object and pass \
        back to the driver. It is possible for different nodes to use different \
        topology keys. This can be empty if driver does not support topology.
    """

    def __init__(
        self,
        name: str,
        node_id: str,
        allocatable: Optional[VolumeNodeResources] = None,
        topology_keys: Optional[List[str]] = None,
    ):
        self.name = name
        self.allocatable = allocatable
        self.nodeID = node_id
        self.topologyKeys = topology_keys


class CSINodeSpec(HelmYaml):
    """
    :param drivers: drivers is a list of information of all CSI Drivers existing on a \
        node. If all drivers in the list are uninstalled, this can become empty.
    """

    def __init__(self, drivers: List[CSINodeDriver]):
        self.drivers = drivers


class StorageClass(Storage):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param provisioner: Provisioner indicates the type of the provisioner.
    :param allow_volume_expansion: AllowVolumeExpansion shows whether the storage class \
        allow volume expand
    :param allowed_topologies: Restrict the node topologies where volumes can be \
        dynamically provisioned. Each volume plugin defines its own supported topology \
        specifications. An empty TopologySelectorTerm list means there is no topology \
        restriction. This field is only honored by servers that enable the \
        VolumeScheduling feature.
    :param parameters: Parameters holds the parameters for the provisioner that should \
        create volumes of this storage class.
    :param volume_binding_mode: VolumeBindingMode indicates how PersistentVolumeClaims \
        should be provisioned and bound.  When unset, VolumeBindingImmediate is used. \
        This field is only honored by servers that enable the VolumeScheduling \
        feature.
    :param mount_options: Dynamically provisioned PersistentVolumes of this storage \
        class are created with these mountOptions, e.g. ["ro", "soft"]. Not validated \
        - mount of the PVs will simply fail if one is invalid.
    :param reclaim_policy: Dynamically provisioned PersistentVolumes of this storage \
        class are created with this reclaimPolicy. Defaults to Delete.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        provisioner: str,
        allow_volume_expansion: Optional[bool] = None,
        allowed_topologies: Optional[List[TopologySelectorTerm]] = None,
        parameters: Optional[dict] = None,
        volume_binding_mode: Optional[str] = None,
        mount_options: Optional[List[str]] = None,
        reclaim_policy: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.allowVolumeExpansion = allow_volume_expansion
        self.allowedTopologies = allowed_topologies
        self.parameters = parameters
        self.provisioner = provisioner
        self.volumeBindingMode = volume_binding_mode
        self.mountOptions = mount_options
        self.reclaimPolicy = reclaim_policy


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
        self,
        inline_volume_spec: Optional[PersistentVolumeSpec] = None,
        persistent_volume_name: Optional[str] = None,
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
        self, attacher: str, source: VolumeAttachmentSource, node_name: str,
    ):
        self.attacher = attacher
        self.source = source
        self.nodeName = node_name


class VolumeAttachment(Storage):
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


class CSIDriverSpec(HelmYaml):
    """
    :param attach_required: attachRequired indicates this CSI volume driver requires an \
        attach operation (because it implements the CSI ControllerPublishVolume() \
        method), and that the Kubernetes attach detach controller should call the \
        attach volume interface which checks the volumeattachment status and waits \
        until the volume is attached before proceeding to mounting. The CSI \
        external-attacher coordinates with CSI volume driver and updates the \
        volumeattachment status when the attach operation is complete. If the \
        CSIDriverRegistry feature gate is enabled and the value is specified to false, \
        the attach operation will be skipped. Otherwise the attach operation will be \
        called.
    :param volume_lifecycle_modes: volumeLifecycleModes defines what kind of volumes \
        this CSI volume driver supports. The default if the list is empty is \
        "Persistent", which is the usage defined by the CSI specification and \
        implemented in Kubernetes via the usual PV/PVC mechanism. The other mode is \
        "Ephemeral". In this mode, volumes are defined inline inside the pod spec with \
        CSIVolumeSource and their lifecycle is tied to the lifecycle of that pod. A \
        driver has to be aware of this because it is only going to get a \
        NodePublishVolume call for such a volume. For more information about \
        implementing this mode, see \
        https://kubernetes-csi.github.io/docs/ephemeral-local-volumes.html A driver \
        can support one or more of these modes and more modes may be added in the \
        future. This field is beta.
    :param pod_info_on_mount: If set to true, podInfoOnMount indicates this CSI volume \
        driver requires additional pod information (like podName, podUID, etc.) during \
        mount operations. If set to false, pod information will not be passed on \
        mount. Default is false. The CSI driver specifies podInfoOnMount as part of \
        driver deployment. If true, Kubelet will pass pod information as VolumeContext \
        in the CSI NodePublishVolume() calls. The CSI driver is responsible for \
        parsing and validating the information passed in as VolumeContext. The \
        following VolumeConext will be passed if podInfoOnMount is set to true. This \
        list might grow, but the prefix will be used. "csi.storage.k8s.io/pod.name": \
        pod.Name "csi.storage.k8s.io/pod.namespace": pod.Namespace \
        "csi.storage.k8s.io/pod.uid": string(pod.UID) "csi.storage.k8s.io/ephemeral": \
        "true" iff the volume is an ephemeral inline volume                            \
             defined by a CSIVolumeSource, otherwise "false"  \
        "csi.storage.k8s.io/ephemeral" is a new feature in Kubernetes 1.16. It is only \
        required for drivers which support both the "Persistent" and "Ephemeral" \
        VolumeLifecycleMode. Other drivers can leave pod info disabled and/or ignore \
        this field. As Kubernetes 1.15 doesn't support this field, drivers can only \
        support one mode when deployed on such a cluster and the deployment determines \
        which mode that is, for example via a command line parameter of the driver.
    """

    def __init__(
        self,
        attach_required: Optional[bool] = None,
        volume_lifecycle_modes: Optional[List[str]] = None,
        pod_info_on_mount: Optional[bool] = None,
    ):
        self.attachRequired = attach_required
        self.volumeLifecycleModes = volume_lifecycle_modes
        self.podInfoOnMount = pod_info_on_mount


class CSINode(Storage):
    """
    :param metadata: metadata.name must be the Kubernetes node name.
    :param spec: spec is the specification of CSINode
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self, metadata: ObjectMeta, spec: CSINodeSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class CSIDriver(Storage):
    """
    :param metadata: Standard object metadata. metadata.Name indicates the name of the \
        CSI driver that this object refers to; it MUST be the same name returned by \
        the CSI GetPluginName() call for that driver. The driver name must be 63 \
        characters or less, beginning and ending with an alphanumeric character \
        ([a-z0-9A-Z]) with dashes (-), dots (.), and alphanumerics between. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: Specification of the CSI Driver.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: CSIDriverSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec
