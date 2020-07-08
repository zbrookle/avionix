from datetime import time
from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.metadata import ListMeta, ObjectMeta
from helm_factory.yaml.yaml_handling import HelmYaml


class NamespaceCondition(HelmYaml):
    """
    :param last_transition_time: None
    :param message: None
    :param reason: None
    :param type: Type of namespace controller condition.
    """

    def __init__(
        self, last_transition_time: time, message: str, reason: str, type: str
    ):
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class NamespaceSpec(HelmYaml):
    """
    :param finalizers: Finalizers is an opaque list of values that must be empty to \
        permanently remove object from storage. More info: \
        https://kubernetes.io/docs/tasks/administer-cluster/namespaces/
    """

    def __init__(self, finalizers: Optional[List[str]] = None):
        self.finalizers = finalizers


class Namespace(KubernetesBaseObject):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    :param spec: Spec defines the behavior of the Namespace. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: NamespaceSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class NamespaceList(KubernetesBaseObject):
    """
    :param items: Items is the list of Namespace objects in the list. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        items: List[Namespace],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
