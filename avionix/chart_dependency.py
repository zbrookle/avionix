from avionix.kubernetes_objects.base_objects import HelmYaml


class ChartDependency(HelmYaml):
    def __init__(self, name: str, version: str, repository: str):
        self.name = name
        self.version = version
        self.repository = repository
