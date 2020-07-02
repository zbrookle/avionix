from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import (
    KubernetesBaseObject,
    Label,
    Annotation,
)


class Deployment(KubernetesBaseObject):
    def __init__(
        self,
        api_version: str,
        name: str,
        namespace: Optional[str] = "",
        labels: Optional[List[Label]] = None,
        annotations: Optional[List[Annotation]] = None,
    ):
        super().__init__(
            api_version, "Deployment", name, namespace, labels, annotations
        )
