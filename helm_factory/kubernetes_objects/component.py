from helm_factory.yaml.yaml_handling import HelmYaml


class ComponentCondition(HelmYaml):
    """
    :param error: Message about the condition for a component. For example, \
        information about a health check.
    :param message: Status of the condition for a component. Valid values for \
        "Healthy": "True", "False", or "Unknown".
    :param type: None
    """

    def __init__(self, error: str, message: str, type: str):
        self.error = error
        self.message = message
        self.type = type
