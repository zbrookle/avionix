from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.pod import PodTemplateSpec
from avionix.kubernetes_objects.selector import LabelSelector
from avionix.kubernetes_objects.volume import PersistentVolumeClaim
from avionix.yaml.yaml_handling import HelmYaml


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
    :param service_name:serviceName is the name of the service that governs this \
        StatefulSet. This service must exist before the StatefulSet, and is \
        responsible for the network identity of the set. Pods get DNS/hostnames that \
        follow the pattern: pod-specific-string.serviceName.default.svc.cluster.local \
        where "pod-specific-string" is managed by the StatefulSet controller.
    :type service_name: str
    :param template:template is the object that describes the pod that will be created \
        if insufficient replicas are detected. Each pod stamped out by the StatefulSet \
        will fulfill this Template, but have a unique identity from the rest of the \
        StatefulSet.
    :type template: PodTemplateSpec
    :param update_strategy:updateStrategy indicates the StatefulSetUpdateStrategy that \
        will be employed to update Pods in the StatefulSet when a revision is made to \
        Template.
    :type update_strategy: StatefulSetUpdateStrategy
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
    :param selector:selector is a label query over pods that should match the replica \
        count. It must match the pod template's labels. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors  # noqa
    :type selector: Optional[LabelSelector]
    """

    def __init__(
        self,
        pod_management_policy: str,
        revision_history_limit: int,
        service_name: str,
        template: PodTemplateSpec,
        update_strategy: StatefulSetUpdateStrategy,
        volume_claim_templates: List[PersistentVolumeClaim],
        replicas: Optional[int] = None,
        selector: Optional[LabelSelector] = None,
    ):
        self.podManagementPolicy = pod_management_policy
        self.revisionHistoryLimit = revision_history_limit
        self.serviceName = service_name
        self.template = template
        self.updateStrategy = update_strategy
        self.volumeClaimTemplates = volume_claim_templates
        self.replicas = replicas
        self.selector = selector


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


class StatefulSet(KubernetesBaseObject):
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


class StatefulSetList(KubernetesBaseObject):
    """
    :param items:None
    :type items: List[StatefulSet]
    :param metadata:None
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[StatefulSet],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
