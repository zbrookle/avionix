from copy import deepcopy
from typing import List, Optional

from yaml import dump


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


class KubernetesKeyValue:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_label_dict(self):
        return {self.key: self.value}


class Label(KubernetesKeyValue):
    def __init__(self, key, value):
        super().__init__(key, value)


class Annotation(KubernetesKeyValue):
    def __init__(self, key, value):
        super().__init__(key, value)


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
