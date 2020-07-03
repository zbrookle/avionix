from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import BaseSpec, KubernetesBaseObject
from helm_factory.kubernetes_objects.key_values_pairs import (
    Annotation,
    Label,
    LabelSelector,
)
from helm_factory.kubernetes_objects.pod import PodTemplateSpec

ROLLING_UPDATE = "RollingUpdate"
RECREATE = "Recreate"


class RollingUpdateDeployment:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#rollingupdatedeployment-v1-apps
    """

    def __init__(self, max_surge: int, max_unavailable: int):
        self.maxSurge = max_surge
        self.maxUnavailable = max_unavailable


class DeploymentStrategy:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#deploymentstrategy-v1-apps
    """

    def __init__(
        self, rolling_update: RollingUpdateDeployment, type: str = ROLLING_UPDATE
    ):
        assert type in [RECREATE, ROLLING_UPDATE]

        if type == ROLLING_UPDATE:
            self.rollingUpdate = rolling_update


class DeploymentSpec(BaseSpec):
    def __init__(
        self,
        min_ready_seconds: Optional[int] = None,
        paused: Optional[bool] = None,
        progress_deadline_seconds: Optional[int] = None,
        replicas: int = 1,
        revision_history_limit: Optional[int] = None,
        selector: Optional[LabelSelector] = None,
        strategy: Optional[DeploymentStrategy] = None,
        pod_template_spec: Optional[PodTemplateSpec] = None,
    ):
        self.minReadySeconds = min_ready_seconds
        self.paused = paused
        self.progressDeadlineSeconds = progress_deadline_seconds
        self.replicas = replicas
        self.revisionHistoryLimit = revision_history_limit
        self.selector = selector
        self.strategy = strategy
        if pod_template_spec:
            self.template = {"spec": pod_template_spec}


class Deployment(KubernetesBaseObject):
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#deploymentspec-v1-apps
    """

    def __init__(
        self,
        api_version: str,
        name: str,
        labels: Optional[List[Label]] = None,
        namespace: Optional[str] = None,
        annotations: Optional[List[Annotation]] = None,
        min_ready_seconds: Optional[int] = None,
        paused: Optional[bool] = None,
        progress_deadline_seconds: Optional[int] = None,
        replicas: int = 1,
        revision_history_limit: Optional[int] = None,
        selector: Optional[LabelSelector] = None,
        strategy: Optional[DeploymentStrategy] = None,
        pod_template_spec: Optional[PodTemplateSpec] = None,
    ):
        super().__init__(
            api_version, "Deployment", name, namespace, labels, annotations
        )
        self.spec = DeploymentSpec(
            min_ready_seconds,
            paused,
            progress_deadline_seconds,
            replicas,
            revision_history_limit,
            selector,
            strategy,
            pod_template_spec,
        )
