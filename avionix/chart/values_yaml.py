from avionix.yaml.yaml_handling import HelmYaml


class Values:
    def __init__(self, values: dict):
        self.values = values


class Value(HelmYaml):
    def __init__(self, value_reference: str):
        self.value_reference = value_reference

    def to_dict(self):
        return "{{" + f" .Values.{self.value_reference} " + "}}"
