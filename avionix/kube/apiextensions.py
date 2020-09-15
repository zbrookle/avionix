"""
Classes for creating custom Kubernetes objects
"""

from typing import List, Optional, Union

from avionix.kube.apiregistration import ServiceReference
from avionix.kube.base_objects import ApiExtensions
from avionix.kube.meta import ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class JSONSchemaPropsOrBool(HelmYaml):
    """"""

    pass


class WebhookClientConfig(HelmYaml):
    """
    :param ca_bundle: caBundle is a PEM encoded CA bundle which will be used to \
        validate the webhook's server certificate. If unspecified, system trust roots \
        on the apiserver are used.
    :param service: service is a reference to the service for this webhook. Either \
        service or url must be specified.  If the webhook is running within the \
        cluster, then you should use `service`.
    :param url: url gives the location of the webhook, in standard URL form \
        (`scheme://host:port/path`). Exactly one of `url` or `service` must be \
        specified.  The `host` should not refer to a service running in the cluster; \
        use the `service` field instead. The host might be resolved via external DNS \
        in some apiservers (e.g., `kube-apiserver` cannot resolve in-cluster DNS as \
        that would be a layering violation). `host` may also be an IP address.  Please \
        note that using `localhost` or `127.0.0.1` as a `host` is risky unless you \
        take great care to run this webhook on all hosts which run an apiserver which \
        might need to make calls to this webhook. Such installs are likely to be \
        non-portable, i.e., not easy to turn up in a new cluster.  The scheme must be \
        "https"; the URL must begin with "https://".  A path is optional, and if \
        present may be any string permissible in a URL. You may use the path to pass \
        an arbitrary string to the webhook, for example, a cluster identifier.  \
        Attempting to use a user or basic auth e.g. "user:password@" is not allowed. \
        Fragments ("#...") and query parameters ("?...") are not allowed, either.
    """

    def __init__(
        self,
        ca_bundle: Optional[str] = None,
        service: Optional[ServiceReference] = None,
        url: Optional[str] = None,
    ):
        self.caBundle = ca_bundle
        self.service = service
        self.url = url


class JSON(HelmYaml):
    """"""

    pass


class JSONSchemaPropsOrArray(HelmYaml):
    """"""

    pass


class ExternalDocumentation(HelmYaml):
    """
    :param url: None
    :param description: None
    """

    def __init__(self, url: str, description: Optional[str] = None):
        self.url = url
        self.description = description


class JSONSchemaProps(HelmYaml):
    """
    :param type: None
    :param additional_items: None
    :param additional_properties: None
    :param all_of: None
    :param any_of: None
    :param default: default is a default value for undefined object fields. Defaulting \
        is a beta feature under the CustomResourceDefaulting feature gate. Defaulting \
        requires spec.preserveUnknownFields to be false.
    :param definitions: None
    :param dependencies: None
    :param description: None
    :param enum: None
    :param example: None
    :param exclusive_maximum: None
    :param exclusive_minimum: None
    :param external_docs: None
    :param format: format is an OpenAPI v3 format string. Unknown formats are ignored. \
        The following formats are validated:  - bsonobjectid: a bson object ID, i.e. a \
        24 characters hex string - uri: an URI as parsed by Golang \
        net/url.ParseRequestURI - email: an email address as parsed by Golang \
        net/mail.ParseAddress - hostname: a valid representation for an Internet host \
        name, as defined by RFC 1034, section 3.1 [RFC1034]. - ipv4: an IPv4 IP as \
        parsed by Golang net.ParseIP - ipv6: an IPv6 IP as parsed by Golang \
        net.ParseIP - cidr: a CIDR as parsed by Golang net.ParseCIDR - mac: a MAC \
        address as parsed by Golang net.ParseMAC - uuid: an UUID that allows uppercase \
        defined by the regex \
        (?i)^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$ - \
        uuid3: an UUID3 that allows uppercase defined by the regex \
        (?i)^[0-9a-f]{8}-?[0-9a-f]{4}-?3[0-9a-f]{3}-?[0-9a-f]{4}-?[0-9a-f]{12}$ - \
        uuid4: an UUID4 that allows uppercase defined by the regex \
        (?i)^[0-9a-f]{8}-?[0-9a-f]{4}-?4[0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}$ \
        - uuid5: an UUID5 that allows uppercase defined by the regex \
        (?i)^[0-9a-f]{8}-?[0-9a-f]{4}-?5[0-9a-f]{3}-?[89ab][0-9a-f]{3}-?[0-9a-f]{12}$ \
        - isbn: an ISBN10 or ISBN13 number string like "0321751043" or \
        "978-0321751041" - isbn10: an ISBN10 number string like "0321751043" - isbn13: \
        an ISBN13 number string like "978-0321751041" - creditcard: a credit card \
        number defined by the regex \
        ^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$  # noqa \
        with any non digit characters mixed in - ssn: a U.S. social security number \
        following the regex ^\d{3}[- ]?\d{2}[- ]?\d{4}$ - hexcolor: an hexadecimal \
        color code like "#FFFFFF: following the regex \
        ^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$ - rgbcolor: an RGB color code like rgb \
        like "rgb(255,255,2559" - byte: base64 encoded binary data - password: any \
        kind of string - date: a date string like "2006-01-02" as defined by full-date \
        in RFC3339 - duration: a duration string like "22 ns" as parsed by Golang \
        time.ParseDuration or compatible with Scala duration format - datetime: a date \
        time string like "2014-12-15T19:30:20.000Z" as defined by date-time in \
        RFC3339.
    :param id: None
    :param items: None
    :param max_items: None
    :param max_length: None
    :param max_properties: None
    :param maximum: None
    :param min_items: None
    :param min_length: None
    :param min_properties: None
    :param minimum: None
    :param multiple_of: None
    :param not_: None
    :param nullable: None
    :param one_of: None
    :param pattern: None
    :param pattern_properties: None
    :param properties: None
    :param required: None
    :param title: None
    :param unique_items: None
    :param x_kubernetes_embedded_resource: x-kubernetes-embedded-resource defines that \
        the value is an embedded Kubernetes runtime.Object, with TypeMeta and \
        ObjectMeta. The type must be object. It is allowed to further restrict the \
        embedded object. kind, apiVersion and metadata are validated automatically. \
        x-kubernetes-preserve-unknown-fields is allowed to be true, but does not have \
        to be if the object is fully specified (up to kind, apiVersion, metadata).
    :param x_kubernetes_int_or_string: x-kubernetes-int-or-string specifies that this \
        value is either an integer or a string. If this is true, an empty type is \
        allowed and type as child of anyOf is permitted if following one of the \
        following patterns:  1) anyOf:    - type: integer    - type: string 2) allOf:  \
          - anyOf:      - type: integer      - type: string    - ... zero or more
    :param x_kubernetes_list_map_keys: x-kubernetes-list-map-keys annotates an array \
        with the x-kubernetes-list-type `map` by specifying the keys used as the index \
        of the map.  This tag MUST only be used on lists that have the \
        "x-kubernetes-list-type" extension set to "map". Also, the values specified \
        for this attribute must be a scalar typed field of the child structure (no \
        nesting is supported).  The properties specified must either be required or \
        have a default value, to ensure those properties are present for all list \
        items.
    :param x_kubernetes_list_type: x-kubernetes-list-type annotates an array to further \
        describe its topology. This extension must only be used on lists and may have \
        3 possible values:
            1) `atomic`: the list is treated as a single entity, like a scalar.
            Atomic lists will be entirely replaced when updated. This extension
            may be used on any type of list (struct, scalar, ...).
            2) `set`: Sets are lists that must not have multiple items with the same \
            value. Each value must be a scalar, an object with x-kubernetes-map-type \
            `atomic` or an array with x-kubernetes-list-type `atomic`.
            3) `map`: These lists are like maps in that their elements have a non-index
            key used to identify them. Order is preserved upon merge. The map tag must \
            only be used on a list with elements of type object. Defaults to atomic
            for arrays.
    :param x_kubernetes_map_type: x-kubernetes-map-type annotates an object to further \
        describe its topology. This extension must only be used when type is object \
        and may have 2 possible values:  1) `granular`:      These maps are actual \
        maps (key-value pairs) and each fields are independent      from each other \
        (they can each be manipulated by separate actors). This is      the default \
        behaviour for all maps. 2) `atomic`: the list is treated as a single entity, \
        like a scalar.      Atomic maps will be entirely replaced when updated.
    :param x_kubernetes_preserve_unknown_fields: x-kubernetes-preserve-unknown-fields \
        stops the API server decoding step from pruning fields which are not specified \
        in the validation schema. This affects fields recursively, but switches back \
        to normal pruning behaviour if nested properties or additionalProperties are \
        specified in the schema. This can either be true or undefined. False is \
        forbidden.
    """

    def __init__(
        self,
        type: Optional[str] = None,
        additional_items: Optional[JSONSchemaPropsOrBool] = None,
        additional_properties: Optional[JSONSchemaPropsOrBool] = None,
        all_of: Optional[List["JSONSchemaProps"]] = None,
        any_of: Optional[List["JSONSchemaProps"]] = None,
        default: Optional[JSON] = None,
        definitions: Optional[dict] = None,
        dependencies: Optional[dict] = None,
        description: Optional[str] = None,
        enum: Optional[List[JSON]] = None,
        example: Optional[JSON] = None,
        exclusive_maximum: Optional[bool] = None,
        exclusive_minimum: Optional[bool] = None,
        external_docs: Optional[ExternalDocumentation] = None,
        format: Optional[str] = None,
        id: Optional[str] = None,
        items: Optional[JSONSchemaPropsOrArray] = None,
        max_items: Optional[int] = None,
        max_length: Optional[int] = None,
        max_properties: Optional[int] = None,
        maximum: Optional[Union[int, float]] = None,
        min_items: Optional[int] = None,
        min_length: Optional[int] = None,
        min_properties: Optional[int] = None,
        minimum: Optional[Union[int, float]] = None,
        multiple_of: Optional[Union[int, float]] = None,
        not_: Optional["JSONSchemaProps"] = None,
        nullable: Optional[bool] = None,
        one_of: Optional[List["JSONSchemaProps"]] = None,
        pattern: Optional[str] = None,
        pattern_properties: Optional[dict] = None,
        properties: Optional[dict] = None,
        required: Optional[List[str]] = None,
        title: Optional[str] = None,
        unique_items: Optional[bool] = None,
        x_kubernetes_embedded_resource: Optional[bool] = None,
        x_kubernetes_int_or_string: Optional[bool] = None,
        x_kubernetes_list_map_keys: Optional[List[str]] = None,
        x_kubernetes_list_type: Optional[str] = None,
        x_kubernetes_map_type: Optional[str] = None,
        x_kubernetes_preserve_unknown_fields: Optional[bool] = None,
    ):
        self.type = type
        self.additionalItems = additional_items
        self.additionalProperties = additional_properties
        self.allOf = all_of
        self.anyOf = any_of
        self.default = default
        self.definitions = definitions
        self.dependencies = dependencies
        self.description = description
        self.enum = enum
        self.example = example
        self.exclusiveMaximum = exclusive_maximum
        self.exclusiveMinimum = exclusive_minimum
        self.externalDocs = external_docs
        self.format = format
        self.id = id
        self.items = items
        self.maxItems = max_items
        self.maxLength = max_length
        self.maxProperties = max_properties
        self.maximum = maximum
        self.minItems = min_items
        self.minLength = min_length
        self.minProperties = min_properties
        self.minimum = minimum
        self.multipleOf = multiple_of
        self["not"] = not_
        self.nullable = nullable
        self.oneOf = one_of
        self.pattern = pattern
        self.patternProperties = pattern_properties
        self.properties = properties
        self.required = required
        self.title = title
        self.uniqueItems = unique_items
        self["x-kubernetes-embedded-resource"] = x_kubernetes_embedded_resource
        self["x-kubernetes-int-or-string"] = x_kubernetes_int_or_string
        self["x-kubernetes-list-map-keys"] = x_kubernetes_list_map_keys
        self["x-kubernetes-list-type"] = x_kubernetes_list_type
        self["x-kubernetes-map-type"] = x_kubernetes_map_type
        self[
            "x-kubernetes-preserve-unknown-fields"
        ] = x_kubernetes_preserve_unknown_fields


class CustomResourceValidation(HelmYaml):
    """
    :param open_apiv3_schema: openAPIV3Schema is the OpenAPI v3 schema to use for \
        validation and pruning.
    """

    def __init__(self, open_apiv3_schema: JSONSchemaProps):
        self.openAPIV3Schema = open_apiv3_schema


class CustomResourceColumnDefinition(HelmYaml):
    """
    :param name: name is a human readable name for the column.
    :param json_path: jsonPath is a simple JSON path (i.e. with array notation) which \
        is evaluated against each custom resource to produce the value for this \
        column.
    :param type: type is an OpenAPI type definition for this column. \
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#data-types \
        for details.
    :param description: description is a human readable description of this column.
    :param format: format is an optional OpenAPI type definition for this column. The \
        'name' format is applied to the primary identifier column to assist in clients \
        identifying column is the resource name. See \
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#data-types \
        for details.
    :param priority: priority is an integer defining the relative importance of this \
        column compared to others. Lower numbers are considered higher priority. \
        Columns that may be omitted in limited space scenarios should be given a \
        priority greater than 0.
    """

    def __init__(
        self,
        name: str,
        json_path: str,
        type: str,
        description: Optional[str] = None,
        format: Optional[str] = None,
        priority: Optional[int] = None,
    ):
        self.name = name
        self.jsonPath = json_path
        self.type = type
        self.description = description
        self.format = format
        self.priority = priority


class CustomResourceSubresourceScale(HelmYaml):
    """
    :param spec_replicas_path: specReplicasPath defines the JSON path inside of a \
        custom resource that corresponds to Scale `spec.replicas`. Only JSON paths \
        without the array notation are allowed. Must be a JSON Path under `.spec`. If \
        there is no value under the given path in the custom resource, the `/scale` \
        subresource will return an error on GET.
    :param status_replicas_path: statusReplicasPath defines the JSON path inside of a \
        custom resource that corresponds to Scale `status.replicas`. Only JSON paths \
        without the array notation are allowed. Must be a JSON Path under `.status`. \
        If there is no value under the given path in the custom resource, the \
        `status.replicas` value in the `/scale` subresource will default to 0.
    :param label_selector_path: labelSelectorPath defines the JSON path inside of a \
        custom resource that corresponds to Scale `status.selector`. Only JSON paths \
        without the array notation are allowed. Must be a JSON Path under `.status` or \
        `.spec`. Must be set to work with HorizontalPodAutoscaler. The field pointed \
        by this JSON path must be a string field (not a complex selector struct) which \
        contains a serialized label selector in string form. More info: \
        https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions#scale-subresource  # noqa \
        If there is no value under the given path in the custom resource, the \
        `status.selector` value in the `/scale` subresource will default to the empty \
        string.
    """

    def __init__(
        self,
        spec_replicas_path: str,
        status_replicas_path: str,
        label_selector_path: Optional[str] = None,
    ):
        self.labelSelectorPath = label_selector_path
        self.specReplicasPath = spec_replicas_path
        self.statusReplicasPath = status_replicas_path


class CustomResourceSubresources(HelmYaml):
    """
    :param scale: scale indicates the custom resource should serve a `/scale` \
        subresource that returns an `autoscaling/v1` Scale object.
    """

    def __init__(self, scale: CustomResourceSubresourceScale):
        self.scale = scale


class CustomResourceDefinitionVersion(HelmYaml):
    """
    :param name: name is the version name, e.g. “v1”, “v2beta1”, etc. The custom \
        resources are served under this version at `/apis/<group>/<version>/...` if \
        `served` is true.
    :param additional_printer_columns: additionalPrinterColumns specifies additional \
        columns returned in Table output. See \
        https://kubernetes.io/docs/reference/using-api/api-concepts/#receiving-resources-as-tables  # noqa \
        for details. If no columns are specified, a single column displaying the age \
        of the custom resource is used.
    :param schema: schema describes the schema used for validation, pruning, and \
        defaulting of this version of the custom resource.
    :param served: served is a flag enabling/disabling this version from being served \
        via REST APIs
    :param storage: storage indicates this version should be used when persisting \
        custom resources to storage. There must be exactly one version with \
        storage=true.
    :param subresources: subresources specify what subresources this version of the \
        defined custom resource have.
    """

    def __init__(
        self,
        name: str,
        additional_printer_columns: List[CustomResourceColumnDefinition],
        schema: CustomResourceValidation,
        served: bool,
        storage: bool,
        subresources: Optional[CustomResourceSubresources] = None,
    ):
        self.name = name
        self.additionalPrinterColumns = additional_printer_columns
        self.schema = schema
        self.served = served
        self.storage = storage
        self.subresources = subresources


class WebhookConversion(HelmYaml):
    """
    :param client_config: clientConfig is the instructions for how to call the webhook \
        if strategy is `Webhook`.
    :param conversion_review_versions: conversionReviewVersions is an ordered list of \
        preferred `ConversionReview` versions the Webhook expects. The API server will \
        use the first version in the list which it supports. If none of the versions \
        specified in this list are supported by API server, conversion will fail for \
        the custom resource. If a persisted Webhook configuration specifies allowed \
        versions and does not include any versions known to the API Server, calls to \
        the webhook will fail.
    """

    def __init__(
        self, client_config: WebhookClientConfig, conversion_review_versions: List[str]
    ):
        self.clientConfig = client_config
        self.conversionReviewVersions = conversion_review_versions


class CustomResourceConversion(HelmYaml):
    """
    :param webhook: webhook describes how to call the conversion webhook. Required when \
        `strategy` is set to `Webhook`.
    :param strategy: strategy specifies how custom resources are converted between \
        versions. Allowed values are:
            - `None`: The converter only change the apiVersion and would not touch any
                other field in the custom resource.
            - `Webhook`: API Server will call to an external webhook to do the
                conversion.

        Additional information is needed for this option. This requires \
        spec.preserveUnknownFields to be false, and spec.conversion.webhook to be set.
    """

    def __init__(self, webhook: WebhookConversion, strategy: str):
        self.webhook = webhook
        self.strategy = strategy


class CustomResourceDefinitionNames(HelmYaml):
    """
    :param categories: categories is a list of grouped resources this custom resource \
        belongs to (e.g. 'all'). This is published in API discovery documents, and \
        used by clients to support invocations like `kubectl get all`.
    :param kind: kind is the serialized kind of the resource. It is normally CamelCase \
        and singular. Custom resource instances will use this value as the `kind` \
        attribute in API calls.
    :param plural: plural is the plural name of the resource to serve. The custom \
        resources are served under `/apis/<group>/<version>/.../<plural>`. Must match \
        the name of the CustomResourceDefinition (in the form \
        `<names.plural>.<group>`). Must be all lowercase.
    :param list_kind: listKind is the serialized kind of the list for this resource. \
        Defaults to `kind` List".
    :param short_names: shortNames are short names for the resource, exposed in API \
        discovery documents, and used by clients to support invocations like `kubectl \
        get <shortname>`. It must be all lowercase.
    :param singular: singular is the singular name of the resource. It must be all \
        lowercase. Defaults to lowercased `kind`.
    """

    def __init__(
        self,
        categories: List[str],
        kind: str,
        plural: str,
        list_kind: Optional[str] = None,
        short_names: Optional[List[str]] = None,
        singular: Optional[str] = None,
    ):
        self.categories = categories
        self.kind = kind
        self.plural = plural
        self.listKind = list_kind
        self.shortNames = short_names
        self.singular = singular


class CustomResourceDefinitionSpec(HelmYaml):
    """
    :param group: group is the API group of the defined custom resource. The custom \
        resources are served under `/apis/<group>/...`. Must match the name of the \
        CustomResourceDefinition (in the form `<names.plural>.<group>`).
    :param names: names specify the resource and kind names for the custom resource.
    :param scope: scope indicates whether the defined custom resource is cluster- or \
        namespace-scoped. Allowed values are `Cluster` and `Namespaced`.
    :param versions: versions is the list of all API versions of the defined custom \
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
    :param conversion: conversion defines conversion settings for the CRD.
    :param preserve_unknown_fields: preserveUnknownFields indicates that object fields \
        which are not specified in the OpenAPI schema should be preserved when \
        persisting to storage. apiVersion, kind, metadata and known fields inside \
        metadata are always preserved. This field is deprecated in favor of setting \
        `x-preserve-unknown-fields` to true in \
        `spec.versions[*].schema.openAPIV3Schema`. See \
        https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions/#pruning-versus-preserving-unknown-fields  # noqa \
        for details.
    """

    def __init__(
        self,
        group: str,
        names: CustomResourceDefinitionNames,
        scope: str,
        versions: List[CustomResourceDefinitionVersion],
        conversion: Optional[CustomResourceConversion] = None,
        preserve_unknown_fields: Optional[bool] = None,
    ):
        self.group = group
        self.names = names
        self.scope = scope
        self.versions = versions
        self.conversion = conversion
        self.preserveUnknownFields = preserve_unknown_fields


class CustomResourceDefinition(ApiExtensions):
    """
    :param metadata: None
    :param spec: spec describes how the user wants the resources to appear
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
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
