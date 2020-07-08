from typing import List, Optional

from helm_factory.options import DEFAULTS
from helm_factory.yaml.yaml_handling import HelmYaml


class LabelSelectorRequirement(HelmYaml):
    """
    :param key: key is the label key that the selector applies to.
    :param operator: operator represents a key's relationship to a set of values. \
        Valid operators are In, NotIn, Exists and DoesNotExist.
    :param values: values is an array of string values. If the operator is In or \
        NotIn, the values array must be non-empty. If the operator is Exists or \
        DoesNotExist, the values array must be empty. This array is replaced during a \
        strategic merge patch.
    """

    def __init__(self, key: str, operator: str, values: List[str]):
        self.key = key
        self.operator = operator
        self.values = values


class LabelSelector(HelmYaml):
    """
    :param match_expressions: matchExpressions is a list of label selector \
        requirements. The requirements are ANDed.
    :param match_labels: matchLabels is a map of {key,value} pairs. A single \
        {key,value} in the matchLabels map is equivalent to an element of \
        matchExpressions, whose key field is "key", the operator is "In", and the \
        values array contains only "value". The requirements are ANDed.
    """

    def __init__(
        self, match_expressions: List[LabelSelectorRequirement], match_labels: dict
    ):
        self.matchExpressions = match_expressions
        self.matchLabels = match_labels


class ResourceFieldSelector(HelmYaml):
    """
    :param container_name: Container name: required for volumes, optional for env vars
    :param resource: Required: resource to select
    :param divisor: Specifies the output format of the exposed resources, defaults to \
        "1"
    """

    def __init__(
        self, container_name: str, resource: str, divisor: Optional[str] = None
    ):
        self.containerName = container_name
        self.resource = resource
        self.divisor = divisor


class ObjectFieldSelector(HelmYaml):
    """
    :param field_path: Path of the field to select in the specified API version.
    :param api_version: Version of the schema the FieldPath is written in terms of, \
        defaults to "v1".
    """

    def __init__(
        self,
        field_path: str,
        api_version: Optional[str] = DEFAULTS["default_api_version"],
    ):
        self.fieldPath = field_path
        self.apiVersion = api_version


class ConfigMapKeySelector(HelmYaml):
    """
    :param key: The key to select.
    :param optional: Specify whether the ConfigMap or its key must be defined
    :param name: Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    """

    def __init__(self, key: str, optional: bool, name: Optional[str] = None):
        self.key = key
        self.optional = optional
        self.name = name


class ScopedResourceSelectorRequirement(HelmYaml):
    """
    :param operator: Represents a scope's relationship to a set of values. Valid \
        operators are In, NotIn, Exists, DoesNotExist.
    :param scope_name: The name of the scope that the selector applies to.
    :param values: An array of string values. If the operator is In or NotIn, the \
        values array must be non-empty. If the operator is Exists or DoesNotExist, the \
        values array must be empty. This array is replaced during a strategic merge \
        patch.
    """

    def __init__(self, operator: str, scope_name: str, values: List[str]):
        self.operator = operator
        self.scopeName = scope_name
        self.values = values


class ScopeSelector(HelmYaml):
    """
    :param match_expressions: A list of scope selector requirements by scope of the \
        resources.
    """

    def __init__(self, match_expressions: List[ScopedResourceSelectorRequirement]):
        self.matchExpressions = match_expressions
