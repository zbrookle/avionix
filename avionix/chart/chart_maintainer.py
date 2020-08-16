from typing import Optional

from avionix.kube.base_objects import HelmYaml


class ChartMaintainer(HelmYaml):
    """
    name: The maintainers name (required for each maintainer)
    email: The maintainers email (optional for each maintainer)
    url: A URL for the maintainer (optional for each maintainer)
    """

    def __init__(
        self, name: str, email: Optional[str] = None, url: Optional[str] = None
    ):
        self.name = name
        self.email = email
        self.url = url
