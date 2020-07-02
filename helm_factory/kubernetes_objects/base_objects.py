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
        uid: str,
        name: str,
        namespace: Optional[str] = "",
        labels: Optional[List[str]] = None,
        annotations: Optional[List[str]] = None,
    ):
        if not labels:
            labels = []
        if not annotations:
            annotations = []
        self.api_version = api_version
        self.kind = kind
        self.metadata = {
            "name": name,
            "labels": labels,
            "annotations": annotations,
            "namespace": namespace,
            "uid": uid,
        }
