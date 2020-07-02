from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject


class Deployment(KubernetesBaseObject):
    def __init__(
        self,
        api_version: str,
        kind: str,
        uid: str,
        name: str,
        namespace: Optional[str] = "",
        labels: Optional[List[str]] = None,
        annotations: Optional[List[str]] = None,
    ):
        super().__init__(
            api_version, "Deployment", uid, name, namespace, labels, annotations
        )


if __name__ == "__main__":
    dep = Deployment("v2", "test", "me", "test")
    print(str(dep))
