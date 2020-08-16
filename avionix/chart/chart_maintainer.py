from typing import Optional

from avionix.kube.base_objects import HelmYaml


class ChartMaintainer(HelmYaml):
    """
    :param name: The maintainers name (required for each maintainer)
    :param email: The maintainers email (optional for each maintainer)
    :param url: A URL for the maintainer (optional for each maintainer)
    """

    def __init__(
        self, name: str, email: Optional[str] = None, url: Optional[str] = None
    ):
        self.name = name
        self.email = email
        self.url = url
