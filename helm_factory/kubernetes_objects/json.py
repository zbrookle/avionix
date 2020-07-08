from typing import List, Optional, Union

from helm_factory.yaml.yaml_handling import HelmYaml


class JSONSchemaPropsOrArray(HelmYaml):
    """
    """

    pass


class ExternalDocumentation(HelmYaml):
    """
    :param description: None
    :param url: None
    """

    def __init__(self, description: str, url: str):
        self.description = description
        self.url = url


class JSON(HelmYaml):
    """
    """

    pass


class JSONSchemaPropsOrBool(HelmYaml):
    """
    """

    pass


class JSONSchemaProps(HelmYaml):
    """
    :param $ref: None
    :param $schema: None
    :param additional_items: None
    :param additional_properties: None
    :param all_of: None
    :param any_of: None
    :param definitions: None
    :param dependencies: None
    :param description: None
    :param enum: None
    :param example: None
    :param exclusive_maximum: None
    :param exclusive_minimum: None
    :param external_docs: None
    :param format: None
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
    :param not: None
    :param nullable: None
    :param one_of: None
    :param pattern: None
    :param pattern_properties: None
    :param properties: None
    :param required: None
    :param title: None
    :param type: None
    :param unique_items: x-kubernetes-embedded-resource defines that the value is an \
        embedded Kubernetes runtime.Object, with TypeMeta and ObjectMeta. The type \
        must be object. It is allowed to further restrict the embedded object. kind, \
        apiVersion and metadata are validated automatically. \
        x-kubernetes-preserve-unknown-fields is allowed to be true, but does not have \
        to be if the object is fully specified (up to kind, apiVersion, metadata).
    :param x_kubernetes_embedded_resource: x-kubernetes-int-or-string specifies that \
        this value is either an integer or a string. If this is true, an empty type is \
        allowed and type as child of anyOf is permitted if following one of the \
        following patterns:  1) anyOf:    - type: integer    - type: string 2) allOf:  \
          - anyOf:      - type: integer      - type: string    - ... zero or more
    :param x_kubernetes_int_or_string: x-kubernetes-list-map-keys annotates an array \
        with the x-kubernetes-list-type `map` by specifying the keys used as the index \
        of the map.  This tag MUST only be used on lists that have the \
        "x-kubernetes-list-type" extension set to "map". Also, the values specified \
        for this attribute must be a scalar typed field of the child structure (no \
        nesting is supported).  The properties specified must either be required or \
        have a default value, to ensure those properties are present for all list \
        items.
    :param x_kubernetes_list_type: x-kubernetes-map-type annotates an object to \
        further describe its topology. This extension must only be used when type is \
        object and may have 2 possible values:  1) `granular`:      These maps are \
        actual maps (key-value pairs) and each fields are independent      from each \
        other (they can each be manipulated by separate actors). This is      the \
        default behaviour for all maps. 2) `atomic`: the list is treated as a single \
        entity, like a scalar.      Atomic maps will be entirely replaced when \
        updated.
    :param x_kubernetes_map_type: x-kubernetes-preserve-unknown-fields stops the API \
        server decoding step from pruning fields which are not specified in the \
        validation schema. This affects fields recursively, but switches back to \
        normal pruning behaviour if nested properties or additionalProperties are \
        specified in the schema. This can either be true or undefined. False is \
        forbidden.
    :param x_kubernetes_preserve_unknown_fields: None
    :param default: default is a default value for undefined object fields. Defaulting \
        is a beta feature under the CustomResourceDefaulting feature gate. Defaulting \
        requires spec.preserveUnknownFields to be false.
    :param x_kubernetes_list_map_keys: x-kubernetes-list-type annotates an array to \
        further describe its topology. This extension must only be used on lists and \
        may have 3 possible values:  1) `atomic`: the list is treated as a single \
        entity, like a scalar.      Atomic lists will be entirely replaced when \
        updated. This extension      may be used on any type of list (struct, scalar, \
        ...). 2) `set`:      Sets are lists that must not have multiple items with the \
        same value. Each      value must be a scalar, an object with \
        x-kubernetes-map-type `atomic` or an      array with x-kubernetes-list-type \
        `atomic`. 3) `map`:      These lists are like maps in that their elements have \
        a non-index key      used to identify them. Order is preserved upon merge. The \
        map tag      must only be used on a list with elements of type object. \
        Defaults to atomic for arrays.
    """

    def __init__(
        self,
        ref: str,
        schema: str,
        additional_items: JSONSchemaPropsOrBool,
        additional_properties: JSONSchemaPropsOrBool,
        all_of: List[JSONSchemaProps],
        any_of: List[JSONSchemaProps],
        definitions: dict,
        dependencies: dict,
        description: str,
        enum: List[JSON],
        example: JSON,
        exclusive_maximum: bool,
        exclusive_minimum: bool,
        external_docs: ExternalDocumentation,
        format: str,
        id: str,
        items: JSONSchemaPropsOrArray,
        max_items: int,
        max_length: int,
        max_properties: int,
        maximum: Union[int, float],
        min_items: int,
        min_length: int,
        min_properties: int,
        minimum: Union[int, float],
        multiple_of: Union[int, float],
        not_: JSONSchemaProps,
        nullable: bool,
        one_of: List[JSONSchemaProps],
        pattern: str,
        pattern_properties: dict,
        properties: dict,
        required: List[str],
        title: str,
        type: str,
        unique_items: bool,
        x_kubernetes_embedded_resource: bool,
        x_kubernetes_int_or_string: bool,
        x_kubernetes_list_type: str,
        x_kubernetes_map_type: str,
        x_kubernetes_preserve_unknown_fields: bool,
        default: Optional[JSON] = None,
        x_kubernetes_list_map_keys: Optional[List[str]] = None,
    ):
        self["$ref"] = ref
        self["$schema"] = schema
        self.additionalItems = additional_items
        self.additionalProperties = additional_properties
        self.allOf = all_of
        self.anyOf = any_of
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
        self.type = type
        self.uniqueItems = unique_items
        self["x-kubernetes-embedded-resource"] = x_kubernetes_embedded_resource
        self["x-kubernetes-int-or-string"] = x_kubernetes_int_or_string
        self["x-kubernetes-list-type"] = x_kubernetes_list_type
        self["x-kubernetes-map-type"] = x_kubernetes_map_type
        self[
            "x-kubernetes-preserve-unknown-fields"
        ] = x_kubernetes_preserve_unknown_fields
        self.default = default
        self["x-kubernetes-list-map-keys"] = x_kubernetes_list_map_keys
