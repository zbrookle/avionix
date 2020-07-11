from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.pod import PodTemplateSpec
from avionix.kubernetes_objects.selector import LabelSelector
from avionix.yaml.yaml_handling import HelmYaml


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
    :param selector:Label selector for pods. Existing ReplicaSets whose pods are \
        selected by this will be the ones affected by this deployment. It must match \
        the pod template's labels.
    :type selector: Optional[LabelSelector]
    :param strategy:The deployment strategy to use to replace existing pods with new \
        ones.
    :type strategy: Optional[DeploymentStrategy]
    """

    def __init__(
        self,
        template: PodTemplateSpec,
        min_ready_seconds: Optional[int] = None,
        paused: Optional[bool] = None,
        progress_deadline_seconds: Optional[int] = None,
        replicas: Optional[int] = None,
        revision_history_limit: Optional[int] = None,
        selector: Optional[LabelSelector] = None,
        strategy: Optional[DeploymentStrategy] = None,
    ):
        self.template = template
        self.minReadySeconds = min_ready_seconds
        self.paused = paused
        self.progressDeadlineSeconds = progress_deadline_seconds
        self.replicas = replicas
        self.revisionHistoryLimit = revision_history_limit
        self.selector = selector
        self.strategy = strategy


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


class Deployment(KubernetesBaseObject):
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


class DeploymentList(KubernetesBaseObject):
    """
    :param items:Items is the list of Deployments.
    :type items: List[Deployment]
    :param metadata:Standard list metadata.
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[Deployment],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
