"""
Classes related to metadata
"""

from datetime import datetime
from typing import List, Optional

from avionix.kube.base_objects import KubernetesBaseObject, Meta
from avionix.yaml.yaml_handling import HelmYaml


class APIResource(Meta):
    """
    :param name: name is the plural name of the resource.
    :param categories: categories is a list of the grouped resources this resource \
        belongs to (e.g. 'all')
    :param group: group is the preferred group of the resource.  Empty implies the \
        group of the containing resource list. For subresources, this may have a \
        different value, for example: Scale".
    :param namespaced: namespaced indicates if a resource is namespaced or not.
    :param short_names: shortNames is a list of suggested short names of the resource.
    :param singular_name: singularName is the singular name of the resource.  This \
        allows clients to handle plural and singular opaquely. The singularName is \
        more correct for reporting status on a single item and both singular and \
        plural are allowed from the kubectl CLI interface.
    :param storage_version_hash: The hash value of the storage version, the version \
        this resource is converted to when written to the data store. Value must be \
        treated as opaque by clients. Only equality comparison on the value is valid. \
        This is an alpha feature and may change or be removed in the future. The field \
        is populated by the apiserver only if the StorageVersionHash feature gate is \
        enabled. This field will remain optional even if it graduates.
    :param verbs: verbs is a list of supported kube verbs (this includes get, list, \
        watch, create, update, patch, delete, deletecollection, and proxy)
    :param version: version is the preferred version of the resource.  Empty implies \
        the version of the containing resource list For subresources, this may have a \
        different value, for example: v1 (while inside a v1beta1 version of the core \
        resource's group)".
    """

    def __init__(
        self,
        name: str,
        categories: List[str],
        group: str,
        namespaced: bool,
        short_names: List[str],
        singular_name: str,
        storage_version_hash: str,
        verbs: List[str],
        version: str,
    ):
        super().__init__()
        self.name = name
        self.categories = categories
        self.group = group
        self.namespaced = namespaced
        self.shortNames = short_names
        self.singularName = singular_name
        self.storageVersionHash = storage_version_hash
        self.verbs = verbs
        self.version = version

    # def to_dict(self):
    #     dictionary = super().to_dict()
    #     del dictionary["apiVersion"]
    #     return dictionary


class ManagedFieldsEntry(HelmYaml):
    """
    :param fields_type: FieldsType is the discriminator for the different fields format \
        and version. There is currently only one possible value: "FieldsV1"
    :param fields_v1: FieldsV1 holds the first JSON version format as described in the \
        "FieldsV1" type.
    :param manager: Manager is an identifier of the workflow managing these fields.
    :param operation: Operation is the type of operation which lead to this \
        ManagedFieldsEntry being created. The only valid values for this field are \
        'Apply' and 'Update'.
    :param time: Time is timestamp of when these fields were set. It should always be \
        empty if Operation is 'Apply'
    :param api_version: APIVersion defines the version of this resource that this field \
        set applies to. The format is "group/version" just like the top-level \
        APIVersion field. It is necessary to track the version of a field set because \
        it cannot be automatically converted.
    """

    def __init__(
        self,
        fields_type: Optional[str] = None,
        fields_v1: Optional[dict] = None,
        manager: Optional[str] = None,
        operation: Optional[str] = None,
        time: Optional[datetime] = None,
        api_version: Optional[str] = None,
    ):
        self.fieldsType = fields_type
        self.fieldsV1 = fields_v1
        self.manager = manager
        self.operation = operation
        self.time = self._get_kube_date_string(time)
        self.apiVersion = api_version

    @staticmethod
    def _get_kube_date_string(datetime_obj: Optional[datetime]):
        return (
            datetime_obj.strftime("%Y-%m-%dT%H:%M:%SZ%Z")
            if datetime_obj
            else datetime_obj
        )


class OwnerReference(KubernetesBaseObject):
    """
    :param name: Name of the referent. More info: \
        http://kubernetes.io/docs/user-guide/identifiers#names
    :param uid: UID of the referent. More info: \
        http://kubernetes.io/docs/user-guide/identifiers#uids
    :param controller: If true, this reference points to the managing controller.
    :param block_owner_deletion: If true, AND if the owner has the "foregroundDeletion" \
        finalizer, then the owner cannot be deleted from the key-value store until \
        this reference is removed. Defaults to false. To set this field, a user needs \
        "delete" permission of the owner, otherwise 422 (Unprocessable Entity) will be \
        returned.
    :param api_version: API version of the referent.
    """

    def __init__(
        self,
        name: str,
        uid: str,
        controller: Optional[bool] = None,
        block_owner_deletion: Optional[bool] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.name = name
        self.controller = controller
        self.blockOwnerDeletion = block_owner_deletion
        self.uid = uid


class ObjectMeta(HelmYaml):
    """
    :param annotations: Annotations is an unstructured key value map stored with a \
        resource that may be set by external tools to store and retrieve arbitrary \
        metadata. They are not queryable and should be preserved when modifying \
        objects. More info: http://kubernetes.io/docs/user-guide/annotations
    :param cluster_name: The name of the cluster which the object belongs to. This is \
        used to distinguish resources with same name and namespace in different \
        clusters. This field is not set anywhere right now and apiserver is going to \
        ignore it if set in create or update request.
    :param finalizers: Must be empty before the object is deleted from the registry. \
        Each entry is an identifier for the responsible component that will remove the \
        entry from the list. If the deletionTimestamp of the object is non-nil, \
        entries in this list can only be removed. Finalizers may be processed and \
        removed in any order.  Order is NOT enforced because it introduces significant \
        risk of stuck finalizers. finalizers is a shared field, any actor with \
        permission can reorder it. If the finalizer list is processed in order, then \
        this can lead to a situation in which the component responsible for the first \
        finalizer in the list is waiting for a signal (field value, external system, \
        or other) produced by a component responsible for a finalizer later in the \
        list, resulting in a deadlock. Without enforced ordering finalizers are free \
        to order amongst themselves and are not vulnerable to ordering changes in the \
        list.
    :param generate_name: GenerateName is an optional prefix, used by the server, to \
        generate a unique name ONLY IF the Name field has not been provided. If this \
        field is used, the name returned to the client will be different than the name \
        passed. This value will also be combined with a unique suffix. The provided \
        value has the same validation rules as the Name field, and may be truncated by \
        the length of the suffix required to make the value unique on the server.  If \
        this field is specified and the generated name exists, the server will NOT \
        return a 409 - instead, it will either return 201 Created or 500 with Reason \
        ServerTimeout indicating a unique name could not be found in the time \
        allotted, and the client should retry (optionally after the time indicated in \
        the Retry-After header).  Applied only if Name is not specified. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#idempotency  # noqa
    :param labels: Map of string keys and values that can be used to organize and \
        categorize (scope and select) objects. May match selectors of replication \
        controllers and services. More info: \
        http://kubernetes.io/docs/user-guide/labels
    :param managed_fields: ManagedFields maps workflow-id and version to the set of \
        fields that are managed by that workflow. This is mostly for internal \
        housekeeping, and users typically shouldn't need to set or understand this \
        field. A workflow can be the user's name, a controller's name, or the name of \
        a specific apply path like "ci-cd". The set of fields is always in the version \
        that the workflow used when modifying the object.
    :param name: Name must be unique within a namespace. Is required when creating \
        resources, although some resources may allow a client to request the \
        generation of an appropriate name automatically. Name is primarily intended \
        for creation idempotence and configuration definition. Cannot be updated. More \
        info: http://kubernetes.io/docs/user-guide/identifiers#names
    :param namespace: Namespace defines the space within each name must be unique. An \
        empty namespace is equivalent to the "default" namespace, but "default" is the \
        canonical representation. Not all objects are required to be scoped to a \
        namespace - the value of this field for those objects will be empty.  Must be \
        a DNS_LABEL. Cannot be updated. More info: \
        http://kubernetes.io/docs/user-guide/namespaces
    :param owner_references: List of objects depended by this object. If ALL objects in \
        the list have been deleted, this object will be garbage collected. If this \
        object is managed by a controller, then an entry in this list will point to \
        this controller, with the controller field set to true. There cannot be more \
        than one managing controller.
    """

    def __init__(
        self,
        annotations: Optional[dict] = None,
        cluster_name: Optional[str] = None,
        finalizers: Optional[List[str]] = None,
        generate_name: Optional[str] = None,
        labels: Optional[dict] = None,
        managed_fields: Optional[List[ManagedFieldsEntry]] = None,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        owner_references: Optional[List[OwnerReference]] = None,
    ):
        self.annotations = annotations
        self.clusterName = cluster_name
        self.finalizers = finalizers
        self.generateName = generate_name
        self.labels = labels
        self.managedFields = managed_fields
        self.name = name
        self.namespace = namespace
        self.ownerReferences = owner_references


class LabelSelectorRequirement(HelmYaml):
    """
    :param key: key is the label key that the selector applies to.
    :param operator: operator represents a key's relationship to a set of values. Valid \
        operators are In, NotIn, Exists and DoesNotExist.
    :param values: values is an array of string values. If the operator is In or NotIn, \
        the values array must be non-empty. If the operator is Exists or DoesNotExist, \
        the values array must be empty. This array is replaced during a strategic \
        merge patch.
    """

    def __init__(self, key: str, operator: str, values: Optional[List[str]] = None):
        self.key = key
        self.operator = operator
        self.values = values


class LabelSelector(HelmYaml):
    """
    :param match_labels: matchLabels is a map of {key,value} pairs. A single \
        {key,value} in the matchLabels map is equivalent to an element of \
        matchExpressions, whose key field is "key", the operator is "In", and the \
        values array contains only "value". The requirements are ANDed.
    :param match_expressions: matchExpressions is a list of label selector \
        requirements. The requirements are ANDed.
    """

    def __init__(
        self,
        match_labels: Optional[dict] = None,
        match_expressions: Optional[List[LabelSelectorRequirement]] = None,
    ):
        self.matchLabels = match_labels
        self.matchExpressions = match_expressions


class ListMeta(HelmYaml):
    """
    :param continue_: continue may be set if the user set a limit on the number of \
        items returned, and indicates that the server has more data available. The \
        value is opaque and may be used to issue another request to the endpoint that \
        served this list to retrieve the next set of available objects. Continuing a \
        consistent list may not be possible if the server configuration has changed or \
        more than a few minutes have passed. The resourceVersion field returned when \
        using this continue value will be identical to the value in the first \
        response, unless you have received this token from an error message.
    :param remaining_item_count: remainingItemCount is the number of subsequent items \
        in the list which are not included in this list response. If the list request \
        contained label or field selectors, then the number of remaining items is \
        unknown and the field will be left unset and omitted during serialization. If \
        the list is complete (either because it is not chunking or because this is the \
        last chunk), then there are no more remaining items and this field will be \
        left unset and omitted during serialization. Servers older than v1.15 do not \
        set this field. The intended use of the remainingItemCount is *estimating* the \
        size of a collection. Clients should not rely on the remainingItemCount to be \
        set or to be exact.
    """

    def __init__(self, continue_: str, remaining_item_count: int):
        self["continue"] = continue_
        self.remainingItemCount = remaining_item_count


class Patch(HelmYaml):
    """"""

    pass


class StatusCause(HelmYaml):
    """
    :param field: The field of the resource that has caused this error, as named by its \
        JSON serialization. May include dot and postfix notation for nested \
        attributes. Arrays are zero-indexed.  Fields may appear more than once in an \
        array of causes due to fields having multiple errors. Optional.  Examples:   \
        "name" - the field "name" on the current resource   "items[0].name" - the \
        field "name" on the first array entry in "items"
    :param message: A human-readable description of the cause of the error.  This field \
        may be presented as-is to a reader.
    :param reason: A machine-readable description of the cause of the error. If this \
        value is empty there is no information available.
    """

    def __init__(self, field: str, message: str, reason: str):
        self.field = field
        self.message = message
        self.reason = reason


class StatusDetails(Meta):
    """
    :param name: The name attribute of the resource associated with the status \
        StatusReason (when there is a single name which can be described).
    :param causes: The Causes array includes more details associated with the \
        StatusReason failure. Not all StatusReasons may provide detailed causes.
    :param group: The group attribute of the resource associated with the status \
        StatusReason.
    :param retry_after_seconds: If specified, the time in seconds before the operation \
        should be retried. Some errors may indicate the client must take an alternate \
        action - for those errors this field may indicate how long to wait before \
        taking the alternate action.
    :param uid: UID of the resource. (when there is a single resource which can be \
        described). More info: http://kubernetes.io/docs/user-guide/identifiers#uids
    """

    def __init__(
        self,
        name: str,
        causes: List[StatusCause],
        group: str,
        retry_after_seconds: Optional[int] = None,
        uid: Optional[str] = None,
    ):
        super().__init__()
        self.name = name
        self.causes = causes
        self.group = group
        self.retryAfterSeconds = retry_after_seconds
        self.uid = uid


class ServerAddressByClientCIDR(HelmYaml):
    """
    :param client_cidr: The CIDR with which clients can match their IP to figure out \
        the server address that they should use.
    :param server_address: Address of this server, suitable for a client that matches \
        the above CIDR. This can be a hostname, hostname:port, IP or IP:port.
    """

    def __init__(self, client_cidr: str, server_address: str):
        self.clientCIDR = client_cidr
        self.serverAddress = server_address


class GroupVersionForDiscovery(HelmYaml):
    """
    :param group_version: groupVersion specifies the API group and version in the form \
        "group/version"
    :param version: version specifies the version in the form of "version". This is to \
        save the clients the trouble of splitting the GroupVersion.
    """

    def __init__(self, group_version: str, version: str):
        self.groupVersion = group_version
        self.version = version


class APIGroup(Meta):
    """
    :param name: name is the name of the group.
    :param preferred_version: preferredVersion is the version preferred by the API \
        server, which probably is the storage version.
    :param server_address_by_client_cidrs: a map of client CIDR to server address that \
        is serving this group. This is to help clients reach servers in the most \
        network-efficient way possible. Clients can use the appropriate server address \
        as per the CIDR that they match. In case of multiple matches, clients should \
        use the longest matching CIDR. The server returns only those CIDRs that it \
        thinks that the client can match. For example: the master will return an \
        internal IP CIDR only, if the client reaches the server using an internal IP. \
        Server looks at X-Forwarded-For header or X-Real-Ip header or \
        request.RemoteAddr (in that order) to get the client IP.
    :param versions: versions are the versions supported in this group.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        name: str,
        preferred_version: GroupVersionForDiscovery,
        server_address_by_client_cidrs: List[ServerAddressByClientCIDR],
        versions: List[GroupVersionForDiscovery],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.name = name
        self.preferredVersion = preferred_version
        self.serverAddressByClientCIDRs = server_address_by_client_cidrs
        self.versions = versions


class Preconditions(HelmYaml):
    """
    :param resource_version: Specifies the target ResourceVersion
    :param uid: Specifies the target UID.
    """

    def __init__(
        self, resource_version: Optional[str] = None, uid: Optional[str] = None
    ):
        self.resourceVersion = resource_version
        self.uid = uid


class DeleteOptions(KubernetesBaseObject):
    """
    :param dry_run: When present, indicates that modifications should not be persisted. \
        An invalid or unrecognized dryRun directive will result in an error response \
        and no further processing of the request. Valid values are: - All: all dry run \
        stages will be processed
    :param orphan_dependents: Deprecated: please use the PropagationPolicy, this field \
        will be deprecated in 1.7. Should the dependent objects be orphaned. If \
        true/false, the "orphan" finalizer will be added to/removed from the object's \
        finalizers list. Either this field or PropagationPolicy may be set, but not \
        both.
    :param preconditions: Must be fulfilled before a deletion is carried out. If not \
        possible, a 409 Conflict status will be returned.
    :param propagation_policy: Whether and how garbage collection will be performed. \
        Either this field or OrphanDependents may be set, but not both. The default \
        policy is decided by the existing finalizer set in the metadata.finalizers and \
        the resource-specific default policy. Acceptable values are: 'Orphan' - orphan \
        the dependents; 'Background' - allow the garbage collector to delete the \
        dependents in the background; 'Foreground' - a cascading policy that deletes \
        all dependents in the foreground.
    :param grace_period_seconds: The duration in seconds before the object should be \
        deleted. Value must be non-negative integer. The value zero indicates delete \
        immediately. If this value is nil, the default grace period for the specified \
        type will be used. Defaults to a per object value if not specified. zero means \
        delete immediately.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        dry_run: List[str],
        orphan_dependents: bool,
        preconditions: Preconditions,
        propagation_policy: str,
        grace_period_seconds: Optional[int] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.dryRun = dry_run
        self.orphanDependents = orphan_dependents
        self.preconditions = preconditions
        self.propagationPolicy = propagation_policy
        self.gracePeriodSeconds = grace_period_seconds


class APIVersions(KubernetesBaseObject):
    """
    :param server_address_by_client_cidrs: a map of client CIDR to server address that \
        is serving this group. This is to help clients reach servers in the most \
        network-efficient way possible. Clients can use the appropriate server address \
        as per the CIDR that they match. In case of multiple matches, clients should \
        use the longest matching CIDR. The server returns only those CIDRs that it \
        thinks that the client can match. For example: the master will return an \
        internal IP CIDR only, if the client reaches the server using an internal IP. \
        Server looks at X-Forwarded-For header or X-Real-Ip header or \
        request.RemoteAddr (in that order) to get the client IP.
    :param versions: versions are the api versions that are available.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        server_address_by_client_cidrs: List[ServerAddressByClientCIDR],
        versions: List[str],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.serverAddressByClientCIDRs = server_address_by_client_cidrs
        self.versions = versions


class Status(KubernetesBaseObject):
    """
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :param code: Suggested HTTP return code for this status, 0 if not set.
    :param message: A human-readable description of the status of this operation.
    :param reason: A machine-readable description of why this operation is in the \
        "Failure" status. If this value is empty there is no information available. A \
        Reason clarifies an HTTP status code but does not override it.
    :param details: Extended data associated with the reason.  Each reason may define \
        its own extended details. This field is optional and the data returned is not \
        guaranteed to conform to any schema except that defined by the reason type.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self,
        metadata: ListMeta,
        code: int,
        message: str,
        reason: str,
        details: Optional[StatusDetails] = None,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.code = code
        self.message = message
        self.reason = reason
        self.details = details


class MicroTime(HelmYaml):
    """"""

    pass


class WatchEvent(HelmYaml):
    """
    :param object: Object is:

        - If Type is Added or Modified: the new state of the object.
        - If Type is Deleted: the state of the object immediately before deletion.
        - If Type is Error: Status is recommended; other types may make sense \
            depending on context.
    :param type: None
    """

    def __init__(self, object: str, type: str):
        self.object = object
        self.type = type


class Time(HelmYaml):
    """"""

    pass
