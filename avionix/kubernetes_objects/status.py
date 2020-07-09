from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta
from avionix.yaml.yaml_handling import HelmYaml


class StatusCause(HelmYaml):
    """
    :param field:The field of the resource that has caused this error, as named by its \
        JSON serialization. May include dot and postfix notation for nested \
        attributes. Arrays are zero-indexed.  Fields may appear more than once in an \
        array of causes due to fields having multiple errors. Optional.  Examples:   \
        "name" - the field "name" on the current resource   "items[0].name" - the \
        field "name" on the first array entry in "items"
    :type field: str
    :param message:A human-readable description of the cause of the error.  This field \
        may be presented as-is to a reader.
    :type message: str
    :param reason:A machine-readable description of the cause of the error. If this \
        value is empty there is no information available.
    :type reason: str
    """

    def __init__(self, field: str, message: str, reason: str):
        self.field = field
        self.message = message
        self.reason = reason


class StatusDetails(KubernetesBaseObject):
    """
    :param causes:The Causes array includes more details associated with the \
        StatusReason failure. Not all StatusReasons may provide detailed causes.
    :type causes: List[StatusCause]
    :param group:The group attribute of the resource associated with the status \
        StatusReason.
    :type group: str
    :param uid:UID of the resource. (when there is a single resource which can be \
        described). More info: http://kubernetes.io/docs/user-guide/identifiers#uids
    :type uid: str
    :param name:The name attribute of the resource associated with the status \
        StatusReason (when there is a single name which can be described).
    :type name: Optional[str]
    :param retry_after_seconds:If specified, the time in seconds before the operation \
        should be retried. Some errors may indicate the client must take an alternate \
        action - for those errors this field may indicate how long to wait before \
        taking the alternate action.
    :type retry_after_seconds: Optional[int]
    """

    def __init__(
        self,
        causes: List[StatusCause],
        group: str,
        uid: str,
        name: Optional[str] = None,
        retry_after_seconds: Optional[int] = None,
    ):
        self.causes = causes
        self.group = group
        self.uid = uid
        self.name = name
        self.retryAfterSeconds = retry_after_seconds


class Status(KubernetesBaseObject):
    """
    :param code:Suggested HTTP return code for this status, 0 if not set.
    :type code: int
    :param message:A human-readable description of the status of this operation.
    :type message: str
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param reason:A machine-readable description of why this operation is in the \
        "Failure" status. If this value is empty there is no information available. A \
        Reason clarifies an HTTP status code but does not override it.
    :type reason: str
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    :param details:Extended data associated with the reason.  Each reason may define \
        its own extended details. This field is optional and the data returned is not \
        guaranteed to conform to any schema except that defined by the reason type.
    :type details: Optional[StatusDetails]
    """

    def __init__(
        self,
        code: int,
        message: str,
        metadata: ListMeta,
        reason: str,
        api_version: Optional[str] = None,
        details: Optional[StatusDetails] = None,
    ):
        super().__init__(api_version)
        self.code = code
        self.message = message
        self.metadata = metadata
        self.reason = reason
        self.details = details
