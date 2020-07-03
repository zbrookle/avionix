from copy import deepcopy
from typing import List, Optional, Union

from yaml import dump

from helm_factory.kubernetes_objects.key_values_pairs import Annotation, Label


class HelmYaml:
    def __clean_nested(self, dictionary_or_list: Union[dict, list]):
        if isinstance(dictionary_or_list, list):
            for i, value in enumerate(dictionary_or_list):
                if isinstance(value, (dict, list)):
                    self.__clean_nested(value)
                elif isinstance(value, HelmYaml):
                    dictionary_or_list[i] = value.to_dict()
        if isinstance(dictionary_or_list, dict):
            for key in list(dictionary_or_list):
                value = dictionary_or_list[key]
                if isinstance(value, (dict, list)) and value:
                    self.__clean_nested(value)
                elif isinstance(value, HelmYaml):
                    dictionary_or_list[key] = value.to_dict()
                elif not value:
                    del dictionary_or_list[key]

    def __str__(self):
        return dump(self.to_dict())

    def to_dict(self):
        dictionary = deepcopy(self.__dict__)
        self.__clean_nested(dictionary)
        return dictionary


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
            "labels": [label.get_label_dict() for label in labels],
            "annotations": [annotation.get_label_dict() for annotation in annotations],
            "namespace": namespace,
        }


class BaseSpec(HelmYaml):
    pass
