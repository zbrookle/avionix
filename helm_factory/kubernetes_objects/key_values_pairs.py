from typing import List

from helm_factory.yaml.yaml_handling import HelmYaml


class KubernetesKeyValue(HelmYaml):
    def __init__(self, key, value):
        assert key is not None and value is not None
        self.key = key
        self.value = value

    def to_dict(self):
        return {self.key: self.value}


class Label(KubernetesKeyValue):
    def __init__(self, key, value):
        super().__init__(key, value)


class Annotation(KubernetesKeyValue):
    def __init__(self, key, value):
        super().__init__(key, value)


class LabelSelectorRequirementArray:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#labelselectorrequirement-v1-meta
    """

    def __init__(self, key: str, operator: str, values: List[str]):
        self.key = key
        self.operator = operator
        self.values = values


class LabelSelector:
    """
    https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.18/#labelselector-v1-meta
    """

    def __init__(self, match_expressions: List, match_labels: List[Label]):
        self.matchExpressions = match_expressions.__dict__
        self.matchLabels = match_labels
