from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.json import JSONSchemaProps
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.webhook import WebhookConversion
from avionix.yaml.yaml_handling import HelmYaml


class CustomResourceValidation(HelmYaml):
    """
    :param open_apiv3_schema:openAPIV3Schema is the OpenAPI v3 schema to use for \
        validation and pruning.
    :type open_apiv3_schema: JSONSchemaProps
    """

    def __init__(self, open_apiv3_schema: JSONSchemaProps):
        self.openAPIV3Schema = open_apiv3_schema


class CustomResourceSubresourceScale(HelmYaml):
    """
    :param label_selector_path:labelSelectorPath defines the JSON path inside of a \
        custom resource that corresponds to Scale `status.selector`. Only JSON paths \
        without the array notation are allowed. Must be a JSON Path under `.status` or \
        `.spec`. Must be set to work with HorizontalPodAutoscaler. The field pointed \
        by this JSON path must be a string field (not a complex selector struct) which \
        contains a serialized label selector in string form. More info: \
        https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions#scale-subresource  # noqa \
        If there is no value under the given path in the custom resource, the \
        `status.selector` value in the `/scale` subresource will default to the empty \
        string.
    :type label_selector_path: str
    :param spec_replicas_path:specReplicasPath defines the JSON path inside of a \
        custom resource that corresponds to Scale `spec.replicas`. Only JSON paths \
        without the array notation are allowed. Must be a JSON Path under `.spec`. If \
        there is no value under the given path in the custom resource, the `/scale` \
        subresource will return an error on GET.
    :type spec_replicas_path: str
    :param status_replicas_path:statusReplicasPath defines the JSON path inside of a \
        custom resource that corresponds to Scale `status.replicas`. Only JSON paths \
        without the array notation are allowed. Must be a JSON Path under `.status`. \
        If there is no value under the given path in the custom resource, the \
        `status.replicas` value in the `/scale` subresource will default to 0.
    :type status_replicas_path: str
    """

    def __init__(
        self,
        label_selector_path: str,
        spec_replicas_path: str,
        status_replicas_path: str,
    ):
        self.labelSelectorPath = label_selector_path
        self.specReplicasPath = spec_replicas_path
        self.statusReplicasPath = status_replicas_path


class CustomResourceDefinitionNames(KubernetesBaseObject):
    """
    :param categories:categories is a list of grouped resources this custom resource \
        belongs to (e.g. 'all'). This is published in API discovery documents, and \
        used by clients to support invocations like `kubectl get all`.
    :type categories: List[str]
    :param plural:plural is the plural name of the resource to serve. The custom \
        resources are served under `/apis/<group>/<version>/.../<plural>`. Must match \
        the name of the CustomResourceDefinition (in the form \
        `<names.plural>.<group>`). Must be all lowercase.
    :type plural: str
    :param short_names:shortNames are short names for the resource, exposed in API \
        discovery documents, and used by clients to support invocations like `kubectl \
        get <shortname>`. It must be all lowercase.
    :type short_names: List[str]
    :param list_kind:listKind is the serialized kind of the list for this resource. \
        Defaults to "`kind`List".
    :type list_kind: Optional[str]
    :param singular:singular is the singular name of the resource. It must be all \
        lowercase. Defaults to lowercased `kind`.
    :type singular: Optional[str]
    """

    def __init__(
        self,
        categories: List[str],
        plural: str,
        short_names: List[str],
        list_kind: Optional[str] = None,
        singular: Optional[str] = None,
    ):
        self.categories = categories
        self.plural = plural
        self.shortNames = short_names
        self.listKind = list_kind
        self.singular = singular


class CustomResourceDefinitionCondition(HelmYaml):
    """
    :param last_transition_time:lastTransitionTime last time the condition \
        transitioned from one status to another.
    :type last_transition_time: time
    :param message:message is a human-readable message indicating details about last \
        transition.
    :type message: str
    :param reason:reason is a unique, one-word, CamelCase reason for the condition's \
        last transition.
    :type reason: str
    :param type:type is the type of the condition. Types include Established, \
        NamesAccepted and Terminating.
    :type type: str
    """

    def __init__(
        self, last_transition_time: time, message: str, reason: str, type: str
    ):
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class CustomResourceConversion(HelmYaml):
    """
    :param webhook:webhook describes how to call the conversion webhook. Required when \
        `strategy` is set to `Webhook`.
    :type webhook: WebhookConversion
    :param strategy:strategy specifies how custom resources are converted between \
        versions. Allowed values are: - `None`: The converter only change the \
        apiVersion and would not touch any other field in the custom resource. - \
        `Webhook`: API Server will call to an external webhook to do the conversion. \
        Additional information   is needed for this option. This requires \
        spec.preserveUnknownFields to be false, and spec.conversion.webhook to be set.
    :type strategy: Optional[str]
    """

    def __init__(self, webhook: WebhookConversion, strategy: Optional[str] = None):
        self.webhook = webhook
        self.strategy = strategy


class CustomResourceColumnDefinition(HelmYaml):
    """
    :param description:description is a human readable description of this column.
    :type description: str
    :param format:format is an optional OpenAPI type definition for this column. The \
        'name' format is applied to the primary identifier column to assist in clients \
        identifying column is the resource name. See \
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#data-types  # noqa \
        for details.
    :type format: str
    :param json_path:jsonPath is a simple JSON path (i.e. with array notation) which \
        is evaluated against each custom resource to produce the value for this \
        column.
    :type json_path: str
    :param type:type is an OpenAPI type definition for this column. See \
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#data-types  # noqa \
        for details.
    :type type: str
    :param name:name is a human readable name for the column.
    :type name: Optional[str]
    :param priority:priority is an integer defining the relative importance of this \
        column compared to others. Lower numbers are considered higher priority. \
        Columns that may be omitted in limited space scenarios should be given a \
        priority greater than 0.
    :type priority: Optional[int]
    """

    def __init__(
        self,
        description: str,
        format: str,
        json_path: str,
        type: str,
        name: Optional[str] = None,
        priority: Optional[int] = None,
    ):
        self.description = description
        self.format = format
        self.jsonPath = json_path
        self.type = type
        self.name = name
        self.priority = priority


class CustomResourceSubresources(HelmYaml):
    """
    :param scale:scale indicates the custom resource should serve a `/scale` \
        subresource that returns an `autoscaling/v1` Scale object.
    :type scale: CustomResourceSubresourceScale
    """

    def __init__(self, scale: CustomResourceSubresourceScale):
        self.scale = scale


class CustomResourceDefinitionVersion(HelmYaml):
    """
    :param additional_printer_columns:additionalPrinterColumns specifies additional \
        columns returned in Table output. See \
        https://kubernetes.io/docs/reference/using-api/api-concepts/#receiving-resources-as-tables  # noqa \
        for details. If no columns are specified, a single column displaying the age \
        of the custom resource is used.
    :type additional_printer_columns: List[CustomResourceColumnDefinition]
    :param schema:schema describes the schema used for validation, pruning, and \
        defaulting of this version of the custom resource.
    :type schema: CustomResourceValidation
    :param served:served is a flag enabling/disabling this version from being served \
        via REST APIs
    :type served: bool
    :param storage:storage indicates this version should be used when persisting \
        custom resources to storage. There must be exactly one version with \
        storage=true.
    :type storage: bool
    :param subresources:subresources specify what subresources this version of the \
        defined custom resource have.
    :type subresources: CustomResourceSubresources
    :param name:name is the version name, e.g. “v1”, “v2beta1”, etc. The custom \
        resources are served under this version at `/apis/<group>/<version>/...` if \
        `served` is true.
    :type name: Optional[str]
    """

    def __init__(
        self,
        additional_printer_columns: List[CustomResourceColumnDefinition],
        schema: CustomResourceValidation,
        served: bool,
        storage: bool,
        subresources: CustomResourceSubresources,
        name: Optional[str] = None,
    ):
        self.additionalPrinterColumns = additional_printer_columns
        self.schema = schema
        self.served = served
        self.storage = storage
        self.subresources = subresources
        self.name = name


class CustomResourceDefinitionSpec(HelmYaml):
    """
    :param conversion:conversion defines conversion settings for the CRD.
    :type conversion: CustomResourceConversion
    :param group:group is the API group of the defined custom resource. The custom \
        resources are served under `/apis/<group>/...`. Must match the name of the \
        CustomResourceDefinition (in the form `<names.plural>.<group>`).
    :type group: str
    :param names:names specify the resource and kind names for the custom resource.
    :type names: CustomResourceDefinitionNames
    :param preserve_unknown_fields:preserveUnknownFields indicates that object fields \
        which are not specified in the OpenAPI schema should be preserved when \
        persisting to storage. apiVersion, kind, metadata and known fields inside \
        metadata are always preserved. This field is deprecated in favor of setting \
        `x-preserve-unknown-fields` to true in \
        `spec.versions[*].schema.openAPIV3Schema`. See \
        https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/#pruning-versus-preserving-unknown-fields  # noqa \
        for details.
    :type preserve_unknown_fields: bool
    :param scope:scope indicates whether the defined custom resource is cluster- or \
        namespace-scoped. Allowed values are `Cluster` and `Namespaced`.
    :type scope: str
    :param versions:versions is the list of all API versions of the defined custom \
        resource. Version names are used to compute the order in which served versions \
        are listed in API discovery. If the version string is "kube-like", it will \
        sort above non "kube-like" version strings, which are ordered \
        lexicographically. "Kube-like" versions start with a "v", then are followed by \
        a number (the major version), then optionally the string "alpha" or "beta" and \
        another number (the minor version). These are sorted first by GA > beta > \
        alpha (where GA is a version with no suffix such as beta or alpha), and then \
        by comparing major version, then minor version. An example sorted list of \
        versions: v10, v2, v1, v11beta2, v10beta3, v3beta1, v12alpha1, v11alpha2, \
        foo1, foo10.
    :type versions: List[CustomResourceDefinitionVersion]
    """

    def __init__(
        self,
        conversion: CustomResourceConversion,
        group: str,
        names: CustomResourceDefinitionNames,
        preserve_unknown_fields: bool,
        scope: str,
        versions: List[CustomResourceDefinitionVersion],
    ):
        self.conversion = conversion
        self.group = group
        self.names = names
        self.preserveUnknownFields = preserve_unknown_fields
        self.scope = scope
        self.versions = versions


class CustomResourceDefinition(KubernetesBaseObject):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:spec describes how the user wants the resources to appear
    :type spec: CustomResourceDefinitionSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: CustomResourceDefinitionSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class CustomResourceDefinitionList(KubernetesBaseObject):
    """
    :param items:items list individual CustomResourceDefinition objects
    :type items: List[CustomResourceDefinition]
    :param metadata:None
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[CustomResourceDefinition],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
