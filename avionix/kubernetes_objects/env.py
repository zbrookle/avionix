from typing import Optional

from avionix.kubernetes_objects.config_map import ConfigMapEnvSource
from avionix.kubernetes_objects.secret import SecretEnvSource, SecretKeySelector
from avionix.kubernetes_objects.selector import (
    ConfigMapKeySelector,
    ObjectFieldSelector,
    ResourceFieldSelector,
)
from avionix.yaml.yaml_handling import HelmYaml


class EnvVarSource(HelmYaml):
    """
    :param config_map_key_ref:Selects a key of a ConfigMap.
    :type config_map_key_ref: ConfigMapKeySelector
    :param field_ref:Selects a field of the pod: supports metadata.name, \
        metadata.namespace, metadata.labels, metadata.annotations, spec.nodeName, \
        spec.serviceAccountName, status.hostIP, status.podIP, status.podIPs.
    :type field_ref: ObjectFieldSelector
    :param resource_field_ref:Selects a resource of the container: only resources \
        limits and requests (limits.cpu, limits.memory, limits.ephemeral-storage, \
        requests.cpu, requests.memory and requests.ephemeral-storage) are currently \
        supported.
    :type resource_field_ref: ResourceFieldSelector
    :param secret_key_ref:Selects a key of a secret in the pod's namespace
    :type secret_key_ref: SecretKeySelector
    """

    def __init__(
        self,
        config_map_key_ref: ConfigMapKeySelector,
        field_ref: ObjectFieldSelector,
        resource_field_ref: ResourceFieldSelector,
        secret_key_ref: SecretKeySelector,
    ):
        self.configMapKeyRef = config_map_key_ref
        self.fieldRef = field_ref
        self.resourceFieldRef = resource_field_ref
        self.secretKeyRef = secret_key_ref


class EnvVar(HelmYaml):
    """
    :param value_from:Source for the environment variable's value. Cannot be used if \
        value is not empty.
    :type value_from: EnvVarSource
    :param name:Name of the environment variable. Must be a C_IDENTIFIER.
    :type name: Optional[str]
    :param value:Variable references $(VAR_NAME) are expanded using the previous \
        defined environment variables in the container and any service environment \
        variables. If a variable cannot be resolved, the reference in the input string \
        will be unchanged. The $(VAR_NAME) syntax can be escaped with a double $$, ie: \
        $$(VAR_NAME). Escaped references will never be expanded, regardless of whether \
        the variable exists or not. Defaults to "".
    :type value: Optional[str]
    """

    def __init__(
        self,
        value_from: EnvVarSource,
        name: Optional[str] = None,
        value: Optional[str] = None,
    ):
        self.valueFrom = value_from
        self.name = name
        self.value = value


class EnvFromSource(HelmYaml):
    """
    :param config_map_ref:The ConfigMap to select from
    :type config_map_ref: ConfigMapEnvSource
    :param prefix:An optional identifier to prepend to each key in the ConfigMap. Must \
        be a C_IDENTIFIER.
    :type prefix: str
    :param secret_ref:The Secret to select from
    :type secret_ref: SecretEnvSource
    """

    def __init__(
        self,
        config_map_ref: ConfigMapEnvSource,
        prefix: str,
        secret_ref: SecretEnvSource,
    ):
        self.configMapRef = config_map_ref
        self.prefix = prefix
        self.secretRef = secret_ref
