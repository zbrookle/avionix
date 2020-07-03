from typing import List, Optional

from helm_factory.kubernetes_objects.key_values_pairs import Annotation, Label
from helm_factory.yaml.yaml_handling import HelmYaml


class KubernetesBaseObject(HelmYaml):
    """
    Base object for other kubernetes objects to inherit from
    Required fields come from
    https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/
    """

    def __init__(
        self,
        api_version: str,
        kind: str,
        name: str,
        namespace: Optional[str] = None,
        labels: Optional[List[Label]] = None,
        annotations: Optional[List[Annotation]] = None,
    ):

        if labels is None:
            labels = []

        if annotations is None:
            annotations = []

        if namespace is None:
            namespace = ""

        self.apiVersion = api_version
        self.kind = kind
        self.metadata = {
            "name": name,
            "labels": labels,
            "annotations": annotations,
            "namespace": namespace,
        }


class BaseSpec(HelmYaml):
    pass
