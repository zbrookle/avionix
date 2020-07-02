from typing import List


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
        self.matchLabels = [label.get_label_dict() for label in match_labels]
