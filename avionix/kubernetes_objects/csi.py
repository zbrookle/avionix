from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.volume import VolumeNodeResources
from avionix.yaml.yaml_handling import HelmYaml


class CSINodeDriver(HelmYaml):
    """
    :param allocatable:allocatable represents the volume resources of a node that are \
        available for scheduling. This field is beta.
    :type allocatable: VolumeNodeResources
    :param node_id:nodeID of the node from the driver point of view. This field \
        enables Kubernetes to communicate with storage systems that do not share the \
        same nomenclature for nodes. For example, Kubernetes may refer to a given node \
        as "node1", but the storage system may refer to the same node as "nodeA". When \
        Kubernetes issues a command to the storage system to attach a volume to a \
        specific node, it can use this field to refer to the node name using the ID \
        that the storage system will understand, e.g. "nodeA" instead of "node1". This \
        field is required.
    :type node_id: str
    :param topology_keys:topologyKeys is the list of keys supported by the driver. \
        When a driver is initialized on a cluster, it provides a set of topology keys \
        that it understands (e.g. "company.com/zone", "company.com/region"). When a \
        driver is initialized on a node, it provides the same topology keys along with \
        values. Kubelet will expose these topology keys as labels on its own node \
        object. When Kubernetes does topology aware provisioning, it can use this list \
        to determine which labels it should retrieve from the node object and pass \
        back to the driver. It is possible for different nodes to use different \
        topology keys. This can be empty if driver does not support topology.
    :type topology_keys: List[str]
    :param name:This is the name of the CSI driver that this object refers to. This \
        MUST be the same name returned by the CSI GetPluginName() call for that \
        driver.
    :type name: Optional[str]
    """

    def __init__(
        self,
        allocatable: VolumeNodeResources,
        node_id: str,
        topology_keys: List[str],
        name: Optional[str] = None,
    ):
        self.allocatable = allocatable
        self.nodeID = node_id
        self.topologyKeys = topology_keys
        self.name = name


class CSIDriverSpec(HelmYaml):
    """
    :param attach_required:attachRequired indicates this CSI volume driver requires an \
        attach operation (because it implements the CSI ControllerPublishVolume() \
        method), and that the Kubernetes attach detach controller should call the \
        attach volume interface which checks the volumeattachment status and waits \
        until the volume is attached before proceeding to mounting. The CSI \
        external-attacher coordinates with CSI volume driver and updates the \
        volumeattachment status when the attach operation is complete. If the \
        CSIDriverRegistry feature gate is enabled and the value is specified to false, \
        the attach operation will be skipped. Otherwise the attach operation will be \
        called.
    :type attach_required: bool
    :param volume_lifecycle_modes:volumeLifecycleModes defines what kind of volumes \
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
    :type volume_lifecycle_modes: List[str]
    :param pod_info_on_mount:If set to true, podInfoOnMount indicates this CSI volume \
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
    :type pod_info_on_mount: Optional[bool]
    """

    def __init__(
        self,
        attach_required: bool,
        volume_lifecycle_modes: List[str],
        pod_info_on_mount: Optional[bool] = None,
    ):
        self.attachRequired = attach_required
        self.volumeLifecycleModes = volume_lifecycle_modes
        self.podInfoOnMount = pod_info_on_mount


class CSIDriver(KubernetesBaseObject):
    """
    :param metadata:Standard object metadata. metadata.Name indicates the name of the \
        CSI driver that this object refers to; it MUST be the same name returned by \
        the CSI GetPluginName() call for that driver. The driver name must be 63 \
        characters or less, beginning and ending with an alphanumeric character \
        ([a-z0-9A-Z]) with dashes (-), dots (.), and alphanumerics between. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the CSI Driver.
    :type spec: CSIDriverSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
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


class CSINodeSpec(HelmYaml):
    """
    :param drivers:drivers is a list of information of all CSI Drivers existing on a \
        node. If all drivers in the list are uninstalled, this can become empty.
    :type drivers: List[CSINodeDriver]
    """

    def __init__(self, drivers: List[CSINodeDriver]):
        self.drivers = drivers


class CSINode(KubernetesBaseObject):
    """
    :param metadata:metadata.name must be the Kubernetes node name.
    :type metadata: ObjectMeta
    :param spec:spec is the specification of CSINode
    :type spec: CSINodeSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: CSINodeSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class CSINodeList(KubernetesBaseObject):
    """
    :param items:items is the list of CSINode
    :type items: List[CSINode]
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
        items: List[CSINode],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class CSIDriverList(KubernetesBaseObject):
    """
    :param items:items is the list of CSIDriver
    :type items: List[CSIDriver]
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
        items: List[CSIDriver],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
