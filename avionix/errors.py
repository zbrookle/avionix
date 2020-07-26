import re


def pre_uninstall_handle_error(message):
    if re.match(r"Error: Kubernetes cluster unreachable.*", message):
        raise ClusterUnavailableError(message)
    if re.match(r"Error: cannot re-use a name that is still in use", message):
        raise ChartAlreadyInstalledError(message)
    if re.match(
        r"Error:.*unable to create new content in namespace \w+ because "
        r"it is being terminated",
        message,
    ):
        raise NamespaceBeingTerminatedError(message)
    raise HelmError(message)


def post_uninstall_handle_error(message):
    raise Exception(message)


class AvionixError(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class ClusterUnavailableError(AvionixError):
    pass


class ChartAlreadyInstalledError(AvionixError):
    pass


class HelmError(AvionixError):
    pass


class NamespaceBeingTerminatedError(AvionixError):
    pass
