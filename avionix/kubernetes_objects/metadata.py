from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.reference import OwnerReference
from avionix.options import DEFAULTS
from avionix.yaml.yaml_handling import HelmYaml


class ListMeta(HelmYaml):
    """
    :param continue_:continue may be set if the user set a limit on the number of \
        items returned, and indicates that the server has more data available. The \
        value is opaque and may be used to issue another request to the endpoint that \
        served this list to retrieve the next set of available objects. Continuing a \
        consistent list may not be possible if the server configuration has changed or \
        more than a few minutes have passed. The resourceVersion field returned when \
        using this continue value will be identical to the value in the first \
        response, unless you have received this token from an error message.
    :type continue_: str
    :param remaining_item_count:remainingItemCount is the number of subsequent items \
        in the list which are not included in this list response. If the list request \
        contained label or field selectors, then the number of remaining items is \
        unknown and the field will be left unset and omitted during serialization. If \
        the list is complete (either because it is not chunking or because this is the \
        last chunk), then there are no more remaining items and this field will be \
        left unset and omitted during serialization. Servers older than v1.15 do not \
        set this field. The intended use of the remainingItemCount is *estimating* the \
        size of a collection. Clients should not rely on the remainingItemCount to be \
        set or to be exact.
    :type remaining_item_count: int
    """

    def __init__(self, continue_: str, remaining_item_count: int):
        self["continue"] = continue_
        self.remainingItemCount = remaining_item_count


class FieldsV1(HelmYaml):
    """
    """

    pass


class ManagedFieldsEntry(HelmYaml):
    """
    :param fields_type:FieldsType is the discriminator for the different fields format \
        and version. There is currently only one possible value: "FieldsV1"
    :type fields_type: str
    :param fields_v1:FieldsV1 holds the first JSON version format as described in the \
        "FieldsV1" type.
    :type fields_v1: FieldsV1
    :param manager:Manager is an identifier of the workflow managing these fields.
    :type manager: str
    :param operation:Operation is the type of operation which lead to this \
        ManagedFieldsEntry being created. The only valid values for this field are \
        'Apply' and 'Update'.
    :type operation: str
    :param time:Time is timestamp of when these fields were set. It should always be \
        empty if Operation is 'Apply'
    :type time: time
    :param api_version:APIVersion defines the version of this resource that this field \
        set applies to. The format is "group/version" just like the top-level \
        APIVersion field. It is necessary to track the version of a field set because \
        it cannot be automatically converted.
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        fields_type: str,
        fields_v1: FieldsV1,
        manager: str,
        operation: str,
        time: time,
        api_version: Optional[str] = DEFAULTS["default_api_version"],
    ):
        self.fieldsType = fields_type
        self.fieldsV1 = fields_v1
        self.manager = manager
        self.operation = operation
        self.time = time
        self.apiVersion = api_version


class ObjectMeta(HelmYaml):
    """
    :param annotations:Annotations is an unstructured key value map stored with a \
        resource that may be set by external tools to store and retrieve arbitrary \
        metadata. They are not queryable and should be preserved when modifying \
        objects. More info: http://kubernetes.io/docs/user-guide/annotations
    :type annotations: Optional[dict]
    :param cluster_name:The name of the cluster which the object belongs to. This is \
        used to distinguish resources with same name and namespace in different \
        clusters. This field is not set anywhere right now and apiserver is going to \
        ignore it if set in create or update request.
    :type cluster_name: Optional[str]
    :param finalizers:Must be empty before the object is deleted from the registry. \
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
    :type finalizers: Optional[List[str]]
    :param generate_name:GenerateName is an optional prefix, used by the server, to \
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
    :type generate_name: Optional[str]
    :param labels:Map of string keys and values that can be used to organize and \
        categorize (scope and select) objects. May match selectors of replication \
        controllers and services. More info: \
        http://kubernetes.io/docs/user-guide/labels
    :type labels: Optional[dict]
    :param managed_fields:ManagedFields maps workflow-id and version to the set of \
        fields that are managed by that workflow. This is mostly for internal \
        housekeeping, and users typically shouldn't need to set or understand this \
        field. A workflow can be the user's name, a controller's name, or the name of \
        a specific apply path like "ci-cd". The set of fields is always in the version \
        that the workflow used when modifying the object.
    :type managed_fields: Optional[List[ManagedFieldsEntry]]
    :param name:Name must be unique within a namespace. Is required when creating \
        resources, although some resources may allow a client to request the \
        generation of an appropriate name automatically. Name is primarily intended \
        for creation idempotence and configuration definition. Cannot be updated. More \
        info: http://kubernetes.io/docs/user-guide/identifiers#names
    :type name: Optional[str]
    :param namespace:Namespace defines the space within each name must be unique. An \
        empty namespace is equivalent to the "default" namespace, but "default" is the \
        canonical representation. Not all objects are required to be scoped to a \
        namespace - the value of this field for those objects will be empty.  Must be \
        a DNS_LABEL. Cannot be updated. More info: \
        http://kubernetes.io/docs/user-guide/namespaces
    :type namespace: Optional[str]
    :param owner_references:List of objects depended by this object. If ALL objects in \
        the list have been deleted, this object will be garbage collected. If this \
        object is managed by a controller, then an entry in this list will point to \
        this controller, with the controller field set to true. There cannot be more \
        than one managing controller.
    :type owner_references: Optional[List[OwnerReference]]
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
