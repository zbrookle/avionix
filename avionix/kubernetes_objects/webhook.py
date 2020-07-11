from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.kubernetes_objects.selector import LabelSelector
from avionix.kubernetes_objects.service import ServiceReference
from avionix.yaml.yaml_handling import HelmYaml


class RuleWithOperations(HelmYaml):
    """
    :param api_groups:APIGroups is the API groups the resources belong to. '\\*' is \
        all groups. If '\\*' is present, the length of the slice must be one. \
        Required.
    :type api_groups: List[str]
    :param api_versions:APIVersions is the API versions the resources belong to. '\\*' \
        is all versions. If '\\*' is present, the length of the slice must be one. \
        Required.
    :type api_versions: List[str]
    :param operations:Operations is the operations the admission hook cares about - \
        CREATE, UPDATE, or * for all operations. If '\\*' is present, the length of \
        the slice must be one. Required.
    :type operations: List[str]
    :param resources:Resources is a list of resources this rule applies to.  For \
        example: 'pods' means pods. 'pods/log' means the log subresource of pods. \
        '\\*' means all resources, but not subresources. 'pods/\\*' means all \
        subresources of pods. '\\*/scale' means all scale subresources. '\\*/\\*' \
        means all resources and their subresources.  If wildcard is present, the \
        validation rule will ensure resources do not overlap with each other.  \
        Depending on the enclosing object, subresources might not be allowed. \
        Required.
    :type resources: Optional[List[str]]
    :param scope:scope specifies the scope of this rule. Valid values are "Cluster", \
        "Namespaced", and "*" "Cluster" means that only cluster-scoped resources will \
        match this rule. Namespace API objects are cluster-scoped. "Namespaced" means \
        that only namespaced resources will match this rule. "*" means that there are \
        no scope restrictions. Subresources match the scope of their parent resource. \
        Default is "*".
    :type scope: Optional[str]
    """

    def __init__(
        self,
        api_groups: List[str],
        api_versions: List[str],
        operations: List[str],
        resources: Optional[List[str]] = None,
        scope: Optional[str] = None,
    ):
        self.apiGroups = api_groups
        self.apiVersions = api_versions
        self.operations = operations
        self.resources = resources
        self.scope = scope


class WebhookClientConfig(HelmYaml):
    """
    :param ca_bundle:caBundle is a PEM encoded CA bundle which will be used to \
        validate the webhook's server certificate. If unspecified, system trust roots \
        on the apiserver are used.
    :type ca_bundle: str
    :param service:service is a reference to the service for this webhook. Either \
        service or url must be specified.  If the webhook is running within the \
        cluster, then you should use `service`.
    :type service: ServiceReference
    :param url:url gives the location of the webhook, in standard URL form \
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
    :type url: Optional[str]
    """

    def __init__(
        self, ca_bundle: str, service: ServiceReference, url: Optional[str] = None
    ):
        self.caBundle = ca_bundle
        self.service = service
        self.url = url


class ValidatingWebhook(HelmYaml):
    """
    :param admission_review_versions:AdmissionReviewVersions is an ordered list of \
        preferred `AdmissionReview` versions the Webhook expects. API server will try \
        to use first version in the list which it supports. If none of the versions \
        specified in this list supported by API server, validation will fail for this \
        object. If a persisted webhook configuration specifies allowed versions and \
        does not include any versions known to the API Server, calls to the webhook \
        will fail and be subject to the failure policy.
    :type admission_review_versions: List[str]
    :param client_config:ClientConfig defines how to communicate with the hook. \
        Required
    :type client_config: WebhookClientConfig
    :param namespace_selector:NamespaceSelector decides whether to run the webhook on \
        an object based on whether the namespace for that object matches the selector. \
        If the object itself is a namespace, the matching is performed on \
        object.metadata.labels. If the object is another cluster scoped resource, it \
        never skips the webhook.  For example, to run the webhook on any objects whose \
        namespace is not associated with "runlevel" of "0" or "1";  you will set the \
        selector as follows: "namespaceSelector": {   "matchExpressions": [     {      \
         "key": "runlevel",       "operator": "NotIn",       "values": [         "0",  \
               "1"       ]     }   ] }  If instead you want to only run the webhook on \
        any objects whose namespace is associated with the "environment" of "prod" or \
        "staging"; you will set the selector as follows: "namespaceSelector": {   \
        "matchExpressions": [     {       "key": "environment",       "operator": \
        "In",       "values": [         "prod",         "staging"       ]     }   ] }  \
        See https://kubernetes.io/docs/concepts/overview/working-with-objects/labels \
        for more examples of label selectors.  Default to the empty LabelSelector, \
        which matches everything.
    :type namespace_selector: LabelSelector
    :param object_selector:ObjectSelector decides whether to run the webhook based on \
        if the object has matching labels. objectSelector is evaluated against both \
        the oldObject and newObject that would be sent to the webhook, and is \
        considered to match if either object matches the selector. A null object \
        (oldObject in the case of create, or newObject in the case of delete) or an \
        object that cannot have labels (like a DeploymentRollback or a PodProxyOptions \
        object) is not considered to match. Use the object selector only if the \
        webhook is opt-in, because end users may skip the admission webhook by setting \
        the labels. Default to the empty LabelSelector, which matches everything.
    :type object_selector: LabelSelector
    :param rules:Rules describes what operations on what resources/subresources the \
        webhook cares about. The webhook cares about an operation if it matches _any_ \
        Rule. However, in order to prevent ValidatingAdmissionWebhooks and \
        MutatingAdmissionWebhooks from putting the cluster in a state which cannot be \
        recovered from without completely disabling the plugin, \
        ValidatingAdmissionWebhooks and MutatingAdmissionWebhooks are never called on \
        admission requests for ValidatingWebhookConfiguration and \
        MutatingWebhookConfiguration objects.
    :type rules: List[RuleWithOperations]
    :param side_effects:SideEffects states whether this webhook has side effects. \
        Acceptable values are: None, NoneOnDryRun (webhooks created via v1beta1 may \
        also specify Some or Unknown). Webhooks with side effects MUST implement a \
        reconciliation system, since a request may be rejected by a future step in the \
        admission change and the side effects therefore need to be undone. Requests \
        with the dryRun attribute will be auto-rejected if they match a webhook with \
        sideEffects == Unknown or Some.
    :type side_effects: str
    :param timeout_seconds:TimeoutSeconds specifies the timeout for this webhook. \
        After the timeout passes, the webhook call will be ignored or the API call \
        will fail based on the failure policy. The timeout value must be between 1 and \
        30 seconds. Default to 10 seconds.
    :type timeout_seconds: int
    :param failure_policy:FailurePolicy defines how unrecognized errors from the \
        admission endpoint are handled - allowed values are Ignore or Fail. Defaults \
        to Fail.
    :type failure_policy: Optional[str]
    :param match_policy:matchPolicy defines how the "rules" list is used to match \
        incoming requests. Allowed values are "Exact" or "Equivalent".  - Exact: match \
        a request only if it exactly matches a specified rule. For example, if \
        deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, \
        but "rules" only included `apiGroups:["apps"], apiVersions:["v1"], resources: \
        ["deployments"]`, a request to apps/v1beta1 or extensions/v1beta1 would not be \
        sent to the webhook.  - Equivalent: match a request if modifies a resource \
        listed in rules, even via another API group or version. For example, if \
        deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, \
        and "rules" only included `apiGroups:["apps"], apiVersions:["v1"], resources: \
        ["deployments"]`, a request to apps/v1beta1 or extensions/v1beta1 would be \
        converted to apps/v1 and sent to the webhook.  Defaults to "Equivalent"
    :type match_policy: Optional[str]
    :param name:The name of the admission webhook. Name should be fully qualified, \
        e.g., imagepolicy.kubernetes.io, where "imagepolicy" is the name of the \
        webhook, and kubernetes.io is the name of the organization. Required.
    :type name: Optional[str]
    """

    def __init__(
        self,
        admission_review_versions: List[str],
        client_config: WebhookClientConfig,
        namespace_selector: LabelSelector,
        object_selector: LabelSelector,
        rules: List[RuleWithOperations],
        side_effects: str,
        timeout_seconds: int,
        failure_policy: Optional[str] = None,
        match_policy: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self.admissionReviewVersions = admission_review_versions
        self.clientConfig = client_config
        self.namespaceSelector = namespace_selector
        self.objectSelector = object_selector
        self.rules = rules
        self.sideEffects = side_effects
        self.timeoutSeconds = timeout_seconds
        self.failurePolicy = failure_policy
        self.matchPolicy = match_policy
        self.name = name


class ValidatingWebhookConfiguration(KubernetesBaseObject):
    """
    :param metadata:Standard object metadata; More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.  # noqa
    :type metadata: ObjectMeta
    :param webhooks:Webhooks is a list of webhooks and the affected resources and \
        operations.
    :type webhooks: List[ValidatingWebhook]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        webhooks: List[ValidatingWebhook],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.webhooks = webhooks


class ValidatingWebhookConfigurationList(KubernetesBaseObject):
    """
    :param items:List of ValidatingWebhookConfiguration.
    :type items: List[ValidatingWebhookConfiguration]
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[ValidatingWebhookConfiguration],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata


class WebhookConversion(HelmYaml):
    """
    :param client_config:clientConfig is the instructions for how to call the webhook \
        if strategy is `Webhook`.
    :type client_config: WebhookClientConfig
    :param conversion_review_versions:conversionReviewVersions is an ordered list of \
        preferred `ConversionReview` versions the Webhook expects. The API server will \
        use the first version in the list which it supports. If none of the versions \
        specified in this list are supported by API server, conversion will fail for \
        the custom resource. If a persisted Webhook configuration specifies allowed \
        versions and does not include any versions known to the API Server, calls to \
        the webhook will fail.
    :type conversion_review_versions: List[str]
    """

    def __init__(
        self, client_config: WebhookClientConfig, conversion_review_versions: List[str]
    ):
        self.clientConfig = client_config
        self.conversionReviewVersions = conversion_review_versions


class MutatingWebhook(HelmYaml):
    """
    :param admission_review_versions:AdmissionReviewVersions is an ordered list of \
        preferred `AdmissionReview` versions the Webhook expects. API server will try \
        to use first version in the list which it supports. If none of the versions \
        specified in this list supported by API server, validation will fail for this \
        object. If a persisted webhook configuration specifies allowed versions and \
        does not include any versions known to the API Server, calls to the webhook \
        will fail and be subject to the failure policy.
    :type admission_review_versions: List[str]
    :param client_config:ClientConfig defines how to communicate with the hook. \
        Required
    :type client_config: WebhookClientConfig
    :param namespace_selector:NamespaceSelector decides whether to run the webhook on \
        an object based on whether the namespace for that object matches the selector. \
        If the object itself is a namespace, the matching is performed on \
        object.metadata.labels. If the object is another cluster scoped resource, it \
        never skips the webhook.  For example, to run the webhook on any objects whose \
        namespace is not associated with "runlevel" of "0" or "1";  you will set the \
        selector as follows: "namespaceSelector": {   "matchExpressions": [     {      \
         "key": "runlevel",       "operator": "NotIn",       "values": [         "0",  \
               "1"       ]     }   ] }  If instead you want to only run the webhook on \
        any objects whose namespace is associated with the "environment" of "prod" or \
        "staging"; you will set the selector as follows: "namespaceSelector": {   \
        "matchExpressions": [     {       "key": "environment",       "operator": \
        "In",       "values": [         "prod",         "staging"       ]     }   ] }  \
        See https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/ \
        for more examples of label selectors.  Default to the empty LabelSelector, \
        which matches everything.
    :type namespace_selector: LabelSelector
    :param object_selector:ObjectSelector decides whether to run the webhook based on \
        if the object has matching labels. objectSelector is evaluated against both \
        the oldObject and newObject that would be sent to the webhook, and is \
        considered to match if either object matches the selector. A null object \
        (oldObject in the case of create, or newObject in the case of delete) or an \
        object that cannot have labels (like a DeploymentRollback or a PodProxyOptions \
        object) is not considered to match. Use the object selector only if the \
        webhook is opt-in, because end users may skip the admission webhook by setting \
        the labels. Default to the empty LabelSelector, which matches everything.
    :type object_selector: LabelSelector
    :param rules:Rules describes what operations on what resources/subresources the \
        webhook cares about. The webhook cares about an operation if it matches _any_ \
        Rule. However, in order to prevent ValidatingAdmissionWebhooks and \
        MutatingAdmissionWebhooks from putting the cluster in a state which cannot be \
        recovered from without completely disabling the plugin, \
        ValidatingAdmissionWebhooks and MutatingAdmissionWebhooks are never called on \
        admission requests for ValidatingWebhookConfiguration and \
        MutatingWebhookConfiguration objects.
    :type rules: List[RuleWithOperations]
    :param side_effects:SideEffects states whether this webhook has side effects. \
        Acceptable values are: None, NoneOnDryRun (webhooks created via v1beta1 may \
        also specify Some or Unknown). Webhooks with side effects MUST implement a \
        reconciliation system, since a request may be rejected by a future step in the \
        admission change and the side effects therefore need to be undone. Requests \
        with the dryRun attribute will be auto-rejected if they match a webhook with \
        sideEffects == Unknown or Some.
    :type side_effects: str
    :param timeout_seconds:TimeoutSeconds specifies the timeout for this webhook. \
        After the timeout passes, the webhook call will be ignored or the API call \
        will fail based on the failure policy. The timeout value must be between 1 and \
        30 seconds. Default to 10 seconds.
    :type timeout_seconds: int
    :param failure_policy:FailurePolicy defines how unrecognized errors from the \
        admission endpoint are handled - allowed values are Ignore or Fail. Defaults \
        to Fail.
    :type failure_policy: Optional[str]
    :param match_policy:matchPolicy defines how the "rules" list is used to match \
        incoming requests. Allowed values are "Exact" or "Equivalent".  - Exact: match \
        a request only if it exactly matches a specified rule. For example, if \
        deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, \
        but "rules" only included `apiGroups:["apps"], apiVersions:["v1"], resources: \
        ["deployments"]`, a request to apps/v1beta1 or extensions/v1beta1 would not be \
        sent to the webhook.  - Equivalent: match a request if modifies a resource \
        listed in rules, even via another API group or version. For example, if \
        deployments can be modified via apps/v1, apps/v1beta1, and extensions/v1beta1, \
        and "rules" only included `apiGroups:["apps"], apiVersions:["v1"], resources: \
        ["deployments"]`, a request to apps/v1beta1 or extensions/v1beta1 would be \
        converted to apps/v1 and sent to the webhook.  Defaults to "Equivalent"
    :type match_policy: Optional[str]
    :param name:The name of the admission webhook. Name should be fully qualified, \
        e.g., imagepolicy.kubernetes.io, where "imagepolicy" is the name of the \
        webhook, and kubernetes.io is the name of the organization. Required.
    :type name: Optional[str]
    :param reinvocation_policy:reinvocationPolicy indicates whether this webhook \
        should be called multiple times as part of a single admission evaluation. \
        Allowed values are "Never" and "IfNeeded".  Never: the webhook will not be \
        called more than once in a single admission evaluation.  IfNeeded: the webhook \
        will be called at least one additional time as part of the admission \
        evaluation if the object being admitted is modified by other admission plugins \
        after the initial webhook call. Webhooks that specify this option *must* be \
        idempotent, able to process objects they previously admitted. Note: * the \
        number of additional invocations is not guaranteed to be exactly one. * if \
        additional invocations result in further modifications to the object, webhooks \
        are not guaranteed to be invoked again. * webhooks that use this option may be \
        reordered to minimize the number of additional invocations. * to validate an \
        object after all mutations are guaranteed complete, use a validating admission \
        webhook instead.  Defaults to "Never".
    :type reinvocation_policy: Optional[str]
    """

    def __init__(
        self,
        admission_review_versions: List[str],
        client_config: WebhookClientConfig,
        namespace_selector: LabelSelector,
        object_selector: LabelSelector,
        rules: List[RuleWithOperations],
        side_effects: str,
        timeout_seconds: int,
        failure_policy: Optional[str] = None,
        match_policy: Optional[str] = None,
        name: Optional[str] = None,
        reinvocation_policy: Optional[str] = None,
    ):
        self.admissionReviewVersions = admission_review_versions
        self.clientConfig = client_config
        self.namespaceSelector = namespace_selector
        self.objectSelector = object_selector
        self.rules = rules
        self.sideEffects = side_effects
        self.timeoutSeconds = timeout_seconds
        self.failurePolicy = failure_policy
        self.matchPolicy = match_policy
        self.name = name
        self.reinvocationPolicy = reinvocation_policy


class MutatingWebhookConfiguration(KubernetesBaseObject):
    """
    :param metadata:Standard object metadata; More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.  # noqa
    :type metadata: ObjectMeta
    :param webhooks:Webhooks is a list of webhooks and the affected resources and \
        operations.
    :type webhooks: List[MutatingWebhook]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        webhooks: List[MutatingWebhook],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.webhooks = webhooks


class MutatingWebhookConfigurationList(KubernetesBaseObject):
    """
    :param items:List of MutatingWebhookConfiguration.
    :type items: List[MutatingWebhookConfiguration]
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds  # noqa
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        items: List[MutatingWebhookConfiguration],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
