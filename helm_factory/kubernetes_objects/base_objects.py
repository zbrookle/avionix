from copy import deepcopy
from typing import List, Optional

from yaml import dump

from helm_factory.kubernetes_objects.key_values_pairs import Annotation, Label


class HelmYaml:
    def __clean_nested(self, dictionary: dict):
        for key in list(dictionary):
            value = dictionary[key]
            if isinstance(value, dict):
                self.__clean_nested(value)
            elif not value:
                del dictionary[key]

    def __str__(self):
        dictionary = deepcopy(self.__dict__)
        self.__clean_nested(dictionary)
        return dump(dictionary)


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
        namespace: Optional[str] = "",
        labels: Optional[List[Label]] = None,
        annotations: Optional[List[Annotation]] = None,
    ):
        if not labels:
            labels = []
        if not annotations:
            annotations = []
        self.apiVersion = api_version
        self.kind = kind
        self.metadata = {
            "name": name,
            "labels": [label.get_label_dict() for label in labels],
            "annotations": [annotation.get_label_dict() for annotation in annotations],
            "namespace": namespace,
        }


class BaseSpec(HelmYaml):
    def to_dict(self):
        return {"spec": self.__dict__}
