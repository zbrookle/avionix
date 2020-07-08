from datetime import time
from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.metadata import ListMeta, ObjectMeta
from helm_factory.kubernetes_objects.pod import PodTemplateSpec
from helm_factory.kubernetes_objects.selector import LabelSelector
from helm_factory.yaml.yaml_handling import HelmYaml


class ReplicaSetCondition(HelmYaml):
    """
    :param last_transition_time: The last time the condition transitioned from one \
        status to another.
    :param message: A human readable message indicating details about the transition.
    :param reason: The reason for the condition's last transition.
    :param type: Type of replica set condition.
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
    :param template: Template is the object that describes the pod that will be \
        created if insufficient replicas are detected. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller#pod-template
    :param min_ready_seconds: Minimum number of seconds for which a newly created pod \
        should be ready without any of its container crashing, for it to be considered \
        available. Defaults to 0 (pod will be considered available as soon as it is \
        ready)
    :param replicas: Replicas is the number of desired replicas. This is a pointer to \
        distinguish between explicit zero and unspecified. Defaults to 1. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/#what-is-a-replicationcontroller
    :param selector: Selector is a label query over pods that should match the replica \
        count. Label keys and values that must match in order to be controlled by this \
        replica set. It must match the pod template's labels. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors
    """

    def __init__(
        self,
        template: PodTemplateSpec,
        min_ready_seconds: Optional[int] = None,
        replicas: Optional[int] = None,
        selector: Optional[LabelSelector] = None,
    ):
        self.template = template
        self.minReadySeconds = min_ready_seconds
        self.replicas = replicas
        self.selector = selector


class ReplicaSet(KubernetesBaseObject):
    """
    :param metadata: If the Labels of a ReplicaSet are empty, they are defaulted to be \
        the same as the Pod(s) that the ReplicaSet manages. Standard object's \
        metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    :param spec: Spec defines the specification of the desired behavior of the \
        ReplicaSet. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
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


class ReplicaSetList(KubernetesBaseObject):
    """
    :param items: List of ReplicaSets. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        items: List[ReplicaSet],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
