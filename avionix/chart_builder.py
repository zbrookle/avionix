from typing import List

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject


class ChartBuilder:
    """
    Main builder object. Accepts kubernetes objects and generates the helm chart
    structure. Can also perform the installation onto the server
    """

    def __init__(self, kubernetes_objects: List[KubernetesBaseObject]):
        self.kubernetes_objects = kubernetes_objects
