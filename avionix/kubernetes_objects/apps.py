from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import Apps
from avionix.kubernetes_objects.core import PersistentVolumeClaim, PodTemplateSpec
from avionix.kubernetes_objects.meta import LabelSelector, ListMeta, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class ReplicaSetCondition(HelmYaml):
    """
    :param last_transition_time:The last time the condition transitioned from one \
        status to another.
    :type last_transition_time: time
    :param message:A human readable message indicating details about the transition.
    :type message: str
    :param reason:The reason for the condition's last transition.
    :type reason: str
    :param type:Type of replica set condition.
    :type type: str
    """

    def __init__(
        self, last_transition_time: time, message: str, reason: str, type: str
    ):
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class ReplicaSetSpec(HelmYaml):
    """
    :param template:Template is the object that describes the pod that will be created \
        if insufficient replicas are detected. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#pod-template  # noqa
    :type template: PodTemplateSpec
    :param selector:Selector is a label query over pods that should match the replica \
        count. Label keys and values that must match in order to be controlled by this \
        replica set. It must match the pod template's labels. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors  # noqa
    :type selector: LabelSelector
    :param min_ready_seconds:Minimum number of seconds for which a newly created pod \
        should be ready without any of its container crashing, for it to be considered \
        available. Defaults to 0 (pod will be considered available as soon as it is \
        ready)
    :type min_ready_seconds: Optional[int]
    :param replicas:Replicas is the number of desired replicas. This is a pointer to \
        distinguish between explicit zero and unspecified. Defaults to 1. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/#what-is-a-replicationcontroller  # noqa
    :type replicas: Optional[int]
    """

    def __init__(
        self,
        template: PodTemplateSpec,
        selector: LabelSelector,
        min_ready_seconds: Optional[int] = None,
        replicas: Optional[int] = None,
    ):
        self.template = template
        self.selector = selector
        self.minReadySeconds = min_ready_seconds
        self.replicas = replicas


class ReplicaSet(Apps):
    """
    :param metadata:If the Labels of a ReplicaSet are empty, they are defaulted to be \
        the same as the Pod(s) that the ReplicaSet manages. Standard object's \
        metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Spec defines the specification of the desired behavior of the \
        ReplicaSet. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: ReplicaSetSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: ReplicaSetSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class RollingUpdateStatefulSetStrategy(HelmYaml):
    """
    :param partition:Partition indicates the ordinal at which the StatefulSet should \
        be partitioned. Default value is 0.
    :type partition: int
    """

    def __init__(self, partition: int):
        self.partition = partition


class StatefulSetUpdateStrategy(HelmYaml):
    """
    :param rolling_update:RollingUpdate is used to communicate parameters when Type is \
        RollingUpdateStatefulSetStrategyType.
    :type rolling_update: RollingUpdateStatefulSetStrategy
    :param type:Type indicates the type of the StatefulSetUpdateStrategy. Default is \
        RollingUpdate.
    :type type: Optional[str]
    """

    def __init__(
        self,
        rolling_update: RollingUpdateStatefulSetStrategy,
        type: Optional[str] = None,
    ):
        self.rollingUpdate = rolling_update
        self.type = type


class StatefulSetSpec(HelmYaml):
    """
    :param template:template is the object that describes the pod that will be created \
        if insufficient replicas are detected. Each pod stamped out by the StatefulSet \
        will fulfill this Template, but have a unique identity from the rest of the \
        StatefulSet.
    :type template: PodTemplateSpec
    :param pod_management_policy:podManagementPolicy controls how pods are created \
        during initial scale up, when replacing pods on nodes, or when scaling down. \
        The default policy is `OrderedReady`, where pods are created in increasing \
        order (pod-0, then pod-1, etc) and the controller will wait until each pod is \
        ready before continuing. When scaling down, the pods are removed in the \
        opposite order. The alternative policy is `Parallel` which will create pods in \
        parallel to match the desired scale without waiting, and on scale down will \
        delete all pods at once.
    :type pod_management_policy: str
    :param revision_history_limit:revisionHistoryLimit is the maximum number of \
        revisions that will be maintained in the StatefulSet's revision history. The \
        revision history consists of all revisions not represented by a currently \
        applied StatefulSetSpec version. The default value is 10.
    :type revision_history_limit: int
    :param selector:selector is a label query over pods that should match the replica \
        count. It must match the pod template's labels. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors  # noqa
    :type selector: LabelSelector
    :param service_name:serviceName is the name of the service that governs this \
        StatefulSet. This service must exist before the StatefulSet, and is \
        responsible for the network identity of the set. Pods get DNS/hostnames that \
        follow the pattern: pod-specific-string.serviceName.default.svc.cluster.local \
        where "pod-specific-string" is managed by the StatefulSet controller.
    :type service_name: str
    :param volume_claim_templates:volumeClaimTemplates is a list of claims that pods \
        are allowed to reference. The StatefulSet controller is responsible for \
        mapping network identities to claims in a way that maintains the identity of a \
        pod. Every claim in this list must have at least one matching (by name) \
        volumeMount in one container in the template. A claim in this list takes \
        precedence over any volumes in the template, with the same name.
    :type volume_claim_templates: List[PersistentVolumeClaim]
    :param replicas:replicas is the desired number of replicas of the given Template. \
        These are replicas in the sense that they are instantiations of the same \
        Template, but individual replicas also have a consistent identity. If \
        unspecified, defaults to 1.
    :type replicas: Optional[int]
    :param update_strategy:updateStrategy indicates the StatefulSetUpdateStrategy that \
        will be employed to update Pods in the StatefulSet when a revision is made to \
        Template.
    :type update_strategy: Optional[StatefulSetUpdateStrategy]
    """

    def __init__(
        self,
        template: PodTemplateSpec,
        pod_management_policy: str,
        revision_history_limit: int,
        selector: LabelSelector,
        service_name: str,
        volume_claim_templates: List[PersistentVolumeClaim],
        replicas: Optional[int] = None,
        update_strategy: Optional[StatefulSetUpdateStrategy] = None,
    ):
        self.template = template
        self.podManagementPolicy = pod_management_policy
        self.revisionHistoryLimit = revision_history_limit
        self.selector = selector
        self.serviceName = service_name
        self.volumeClaimTemplates = volume_claim_templates
        self.replicas = replicas
        self.updateStrategy = update_strategy


class RollingUpdateDeployment(HelmYaml):
    """
    :param max_surge:The maximum number of pods that can be scheduled above the \
        desired number of pods. Value can be an absolute number (ex: 5) or a \
        percentage of desired pods (ex: 10%). This can not be 0 if MaxUnavailable is \
        0. Absolute number is calculated from percentage by rounding up. Defaults to \
        25%. Example: when this is set to 30%, the new ReplicaSet can be scaled up \
        immediately when the rolling update starts, such that the total number of old \
        and new pods do not exceed 130% of desired pods. Once old pods have been \
        killed, new ReplicaSet can be scaled up further, ensuring that total number of \
        pods running at any time during the update is at most 130% of desired pods.
    :type max_surge: Optional[str]
    :param max_unavailable:The maximum number of pods that can be unavailable during \
        the update. Value can be an absolute number (ex: 5) or a percentage of desired \
        pods (ex: 10%). Absolute number is calculated from percentage by rounding \
        down. This can not be 0 if MaxSurge is 0. Defaults to 25%. Example: when this \
        is set to 30%, the old ReplicaSet can be scaled down to 70% of desired pods \
        immediately when the rolling update starts. Once new pods are ready, old \
        ReplicaSet can be scaled down further, followed by scaling up the new \
        ReplicaSet, ensuring that the total number of pods available at all times \
        during the update is at least 70% of desired pods.
    :type max_unavailable: Optional[str]
    """

    def __init__(
        self, max_surge: Optional[str] = None, max_unavailable: Optional[str] = None
    ):
        self.maxSurge = max_surge
        self.maxUnavailable = max_unavailable


class DeploymentStrategy(HelmYaml):
    """
    :param rolling_update:Rolling update config params. Present only if \
        DeploymentStrategyType = RollingUpdate.
    :type rolling_update: Optional[RollingUpdateDeployment]
    :param type:Type of deployment. Can be "Recreate" or "RollingUpdate". Default is \
        RollingUpdate.
    :type type: Optional[str]
    """

    def __init__(
        self,
        rolling_update: Optional[RollingUpdateDeployment] = None,
        type: Optional[str] = None,
    ):
        self.rollingUpdate = rolling_update
        self.type = type


class DeploymentSpec(HelmYaml):
    """
    :param template:Template describes the pods that will be created.
    :type template: PodTemplateSpec
    :param selector:Label selector for pods. Existing ReplicaSets whose pods are \
        selected by this will be the ones affected by this deployment. It must match \
        the pod template's labels.
    :type selector: LabelSelector
    :param min_ready_seconds:Minimum number of seconds for which a newly created pod \
        should be ready without any of its container crashing, for it to be considered \
        available. Defaults to 0 (pod will be considered available as soon as it is \
        ready)
    :type min_ready_seconds: Optional[int]
    :param paused:Indicates that the deployment is paused.
    :type paused: Optional[bool]
    :param progress_deadline_seconds:The maximum time in seconds for a deployment to \
        make progress before it is considered to be failed. The deployment controller \
        will continue to process failed deployments and a condition with a \
        ProgressDeadlineExceeded reason will be surfaced in the deployment status. \
        Note that progress will not be estimated during the time a deployment is \
        paused. Defaults to 600s.
    :type progress_deadline_seconds: Optional[int]
    :param replicas:Number of desired pods. This is a pointer to distinguish between \
        explicit zero and not specified. Defaults to 1.
    :type replicas: Optional[int]
    :param revision_history_limit:The number of old ReplicaSets to retain to allow \
        rollback. This is a pointer to distinguish between explicit zero and not \
        specified. Defaults to 10.
    :type revision_history_limit: Optional[int]
    :param strategy:The deployment strategy to use to replace existing pods with new \
        ones.
    :type strategy: Optional[DeploymentStrategy]
    """

    def __init__(
        self,
        template: PodTemplateSpec,
        selector: LabelSelector,
        min_ready_seconds: Optional[int] = None,
        paused: Optional[bool] = None,
        progress_deadline_seconds: Optional[int] = None,
        replicas: Optional[int] = None,
        revision_history_limit: Optional[int] = None,
        strategy: Optional[DeploymentStrategy] = None,
    ):
        self.template = template
        self.selector = selector
        self.minReadySeconds = min_ready_seconds
        self.paused = paused
        self.progressDeadlineSeconds = progress_deadline_seconds
        self.replicas = replicas
        self.revisionHistoryLimit = revision_history_limit
        self.strategy = strategy


class StatefulSetCondition(HelmYaml):
    """
    :param last_transition_time:Last time the condition transitioned from one status \
        to another.
    :type last_transition_time: time
    :param message:A human readable message indicating details about the transition.
    :type message: str
    :param reason:The reason for the condition's last transition.
    :type reason: str
    :param type:Type of statefulset condition.
    :type type: str
    """

    def __init__(
        self, last_transition_time: time, message: str, reason: str, type: str
    ):
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class StatefulSet(Apps):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:Spec defines the desired identities of pods in this set.
    :type spec: StatefulSetSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: StatefulSetSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class StatefulSetList(Apps):
    """
    :param metadata:None
    :type metadata: ListMeta
    :param items:None
    :type items: List[StatefulSet]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[StatefulSet],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class DeploymentCondition(HelmYaml):
    """
    :param last_transition_time:Last time the condition transitioned from one status \
        to another.
    :type last_transition_time: time
    :param last_update_time:The last time this condition was updated.
    :type last_update_time: time
    :param message:A human readable message indicating details about the transition.
    :type message: str
    :param reason:The reason for the condition's last transition.
    :type reason: str
    :param type:Type of deployment condition.
    :type type: str
    """

    def __init__(
        self,
        last_transition_time: time,
        last_update_time: time,
        message: str,
        reason: str,
        type: str,
    ):
        self.lastTransitionTime = last_transition_time
        self.lastUpdateTime = last_update_time
        self.message = message
        self.reason = reason
        self.type = type


class Deployment(Apps):
    """
    :param metadata:Standard object metadata.
    :type metadata: ObjectMeta
    :param spec:Specification of the desired behavior of the Deployment.
    :type spec: DeploymentSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: DeploymentSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class DeploymentList(Apps):
    """
    :param metadata:Standard list metadata.
    :type metadata: ListMeta
    :param items:Items is the list of Deployments.
    :type items: List[Deployment]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[Deployment],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class DaemonSetCondition(HelmYaml):
    """
    :param last_transition_time:Last time the condition transitioned from one status \
        to another.
    :type last_transition_time: time
    :param message:A human readable message indicating details about the transition.
    :type message: str
    :param reason:The reason for the condition's last transition.
    :type reason: str
    :param type:Type of DaemonSet condition.
    :type type: str
    """

    def __init__(
        self, last_transition_time: time, message: str, reason: str, type: str
    ):
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class ControllerRevision(Apps):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param data:Data is the serialized representation of the state.
    :type data: str
    :param revision:Revision indicates the revision of the state represented by Data.
    :type revision: int
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        data: str,
        revision: int,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.data = data
        self.revision = revision


class ControllerRevisionList(Apps):
    """
    :param metadata:More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param items:Items is the list of ControllerRevisions
    :type items: List[ControllerRevision]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[ControllerRevision],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class ReplicaSetList(Apps):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param items:List of ReplicaSets. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller  # noqa
    :type items: List[ReplicaSet]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[ReplicaSet],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class RollingUpdateDaemonSet(HelmYaml):
    """
    :param max_unavailable:The maximum number of DaemonSet pods that can be \
        unavailable during the update. Value can be an absolute number (ex: 5) or a \
        percentage of total number of DaemonSet pods at the start of the update (ex: \
        10%). Absolute number is calculated from percentage by rounding up. This \
        cannot be 0. Default value is 1. Example: when this is set to 30%, at most 30% \
        of the total number of nodes that should be running the daemon pod (i.e. \
        status.desiredNumberScheduled) can have their pods stopped for an update at \
        any given time. The update starts by stopping at most 30% of those DaemonSet \
        pods and then brings up new DaemonSet pods in their place. Once the new pods \
        are available, it then proceeds onto other DaemonSet pods, thus ensuring that \
        at least 70% of original number of DaemonSet pods are available at all times \
        during the update.
    :type max_unavailable: str
    """

    def __init__(self, max_unavailable: str):
        self.maxUnavailable = max_unavailable


class DaemonSetUpdateStrategy(HelmYaml):
    """
    :param rolling_update:Rolling update config params. Present only if type = \
        "RollingUpdate".
    :type rolling_update: Optional[RollingUpdateDaemonSet]
    :param type:Type of daemon set update. Can be "RollingUpdate" or "OnDelete". \
        Default is RollingUpdate.
    :type type: Optional[str]
    """

    def __init__(
        self,
        rolling_update: Optional[RollingUpdateDaemonSet] = None,
        type: Optional[str] = None,
    ):
        self.rollingUpdate = rolling_update
        self.type = type


class DaemonSetSpec(HelmYaml):
    """
    :param template:An object that describes the pod that will be created. The \
        DaemonSet will create exactly one copy of this pod on every node that matches \
        the template's node selector (or on every node if no node selector is \
        specified). More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#pod-template  # noqa
    :type template: PodTemplateSpec
    :param selector:A label query over pods that are managed by the daemon set. Must \
        match in order to be controlled. It must match the pod template's labels. More \
        info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors  # noqa
    :type selector: LabelSelector
    :param min_ready_seconds:The minimum number of seconds for which a newly created \
        DaemonSet pod should be ready without any of its container crashing, for it to \
        be considered available. Defaults to 0 (pod will be considered available as \
        soon as it is ready).
    :type min_ready_seconds: Optional[int]
    :param revision_history_limit:The number of old history to retain to allow \
        rollback. This is a pointer to distinguish between explicit zero and not \
        specified. Defaults to 10.
    :type revision_history_limit: Optional[int]
    :param update_strategy:An update strategy to replace existing DaemonSet pods with \
        new pods.
    :type update_strategy: Optional[DaemonSetUpdateStrategy]
    """

    def __init__(
        self,
        template: PodTemplateSpec,
        selector: LabelSelector,
        min_ready_seconds: Optional[int] = None,
        revision_history_limit: Optional[int] = None,
        update_strategy: Optional[DaemonSetUpdateStrategy] = None,
    ):
        self.template = template
        self.selector = selector
        self.minReadySeconds = min_ready_seconds
        self.revisionHistoryLimit = revision_history_limit
        self.updateStrategy = update_strategy


class DaemonSet(Apps):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:The desired behavior of this daemon set. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: DaemonSetSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: DaemonSetSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class DaemonSetList(Apps):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param items:A list of daemon sets.
    :type items: List[DaemonSet]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ListMeta,
        items: List[DaemonSet],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items
