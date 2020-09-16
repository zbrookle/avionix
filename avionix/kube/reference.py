"""
Contains ObjectReference class
"""

from typing import Optional

from avionix.kube.base_objects import Core


class ObjectReference(Core):
    """
    :param field_path: If referring to a piece of an object instead of an entire \
        object, this string should contain a valid JSON/Go field access statement, \
        such as desiredState.manifest.containers[2]. For example, if the object \
        reference is to a container within a pod, this would take on a value like: \
        "spec.containers{name}" (where "name" refers to the name of the container that \
        triggered the event) or if no container name is specified "spec.containers[2]" \
        (container with index 2 in this pod). This syntax is chosen only to have some \
        well-defined way of referencing a part of an object.
    :param name: Name of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa
    :param namespace: Namespace of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
    :param resource_version: Specific resourceVersion to which this reference is made, \
        if any. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#concurrency-control-and-consistency  # noqa
    :param uid: UID of the referent. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids
    :param api_version: API version of the referent.
    """

    def __init__(
        self,
        field_path: str,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        resource_version: Optional[str] = None,
        uid: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.fieldPath = field_path
        self.name = name
        self.namespace = namespace
        self.resourceVersion = resource_version
        self.uid = uid
