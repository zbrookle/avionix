from typing import List, Optional

from yaml import YAMLObject, dump


class KubernetesBaseObject(YAMLObject):
    """
    Base object for other kubernetes objects to inherit from
    """

    yaml_tag = "KubeObject"

    def __init__(
        self,
        api_version: str,
        kind: str,
        name: Optional[str],
        labels: Optional[List[str]] = None,
        annotations: Optional[List[str]] = None,
    ):
        self.api_version = api_version
        self.kind = kind
        self.name = name
        self.labels = labels
        self.annotations = annotations

    def __str__(self):
        return dump(self)
