from typing import Optional

from avionix.yaml.yaml_handling import HelmYaml


class KeyToPath(HelmYaml):
    """
    :param key:The key to project.
    :type key: str
    :param path:The relative path of the file to map the key to. May not be an \
        absolute path. May not contain the path element '..'. May not start with the \
        string '..'.
    :type path: str
    :param mode:Optional: mode bits to use on this file, must be a value between 0 and \
        0777. If not specified, the volume defaultMode will be used. This might be in \
        conflict with other options that affect the file mode, like fsGroup, and the \
        result can be other mode bits set.
    :type mode: Optional[int]
    """

    def __init__(self, key: str, path: str, mode: Optional[int] = None):
        self.key = key
        self.path = path
        self.mode = mode


class ResourceRequirements(HelmYaml):
    """
    :param limits:Limits describes the maximum amount of compute resources allowed. \
        More info: \
        https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/  # noqa
    :type limits: dict
    :param requests:Requests describes the minimum amount of compute resources \
        required. If Requests is omitted for a container, it defaults to Limits if \
        that is explicitly specified, otherwise to an implementation-defined value. \
        More info: \
        https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/  # noqa
    :type requests: Optional[dict]
    """

    def __init__(self, limits: dict, requests: Optional[dict] = None):
        self.limits = limits
        self.requests = requests


class Patch(HelmYaml):
    """
    """

    pass
