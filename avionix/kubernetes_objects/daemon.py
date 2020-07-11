from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.pod import PodTemplateSpec
from avionix.kubernetes_objects.selector import LabelSelector
from avionix.yaml.yaml_handling import HelmYaml


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
    :param update_strategy:An update strategy to replace existing DaemonSet pods with \
        new pods.
    :type update_strategy: DaemonSetUpdateStrategy
    :param min_ready_seconds:The minimum number of seconds for which a newly created \
        DaemonSet pod should be ready without any of its container crashing, for it to \
        be considered available. Defaults to 0 (pod will be considered available as \
        soon as it is ready).
    :type min_ready_seconds: Optional[int]
    :param revision_history_limit:The number of old history to retain to allow \
        rollback. This is a pointer to distinguish between explicit zero and not \
        specified. Defaults to 10.
    :type revision_history_limit: Optional[int]
    :param selector:A label query over pods that are managed by the daemon set. Must \
        match in order to be controlled. It must match the pod template's labels. More \
        info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors  # noqa
    :type selector: Optional[LabelSelector]
    """

    def __init__(
        self,
        template: PodTemplateSpec,
        update_strategy: DaemonSetUpdateStrategy,
        min_ready_seconds: Optional[int] = None,
        revision_history_limit: Optional[int] = None,
        selector: Optional[LabelSelector] = None,
    ):
        self.template = template
        self.updateStrategy = update_strategy
        self.minReadySeconds = min_ready_seconds
        self.revisionHistoryLimit = revision_history_limit
        self.selector = selector


class DaemonSet(KubernetesBaseObject):
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


class DaemonSetList(KubernetesBaseObject):
    """
    :param items:A list of daemon sets.
    :type items: List[DaemonSet]
    :param metadata:Standard list metadata. More info: \
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
        items: List[DaemonSet],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
