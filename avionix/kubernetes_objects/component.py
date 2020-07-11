from avionix.yaml.yaml_handling import HelmYaml


class ComponentCondition(HelmYaml):
    """
    :param error:Condition error code for a component. For example, a health check \
        error code.
    :type error: str
    :param message:Message about the condition for a component. For example, \
        information about a health check.
    :type message: str
    :param type:Type of condition for a component. Valid value: "Healthy"
    :type type: str
    """

    def __init__(self, error: str, message: str, type: str):
        self.error = error
        self.message = message
        self.type = type
