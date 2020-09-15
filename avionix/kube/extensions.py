"""
Classes related to Ingress
"""

from typing import List, Optional

from avionix.kube.base_objects import Extensions
from avionix.kube.core import TypedLocalObjectReference
from avionix.kube.meta import ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class IngressTLS(HelmYaml):
    """
    :param secret_name: SecretName is the name of the secret used to terminate SSL \
        traffic on 443. Field is left optional to allow SSL routing based on SNI \
        hostname alone. If the SNI host in a listener conflicts with the "Host" header \
        field used by an IngressRule, the SNI host is used for termination and value \
        of the Host header is used for routing.
    :param hosts: Hosts are a list of hosts included in the TLS certificate. The values \
        in this list must match the name/s used in the tlsSecret. Defaults to the \
        wildcard host setting for the loadbalancer controller fulfilling this Ingress, \
        if left unspecified.
    """

    def __init__(self, secret_name: str, hosts: Optional[List[str]] = None):
        self.secretName = secret_name
        self.hosts = hosts


class IngressBackend(HelmYaml):
    """
    :param service_name: Specifies the name of the referenced service.
    :param service_port: Specifies the port of the referenced service.
    :param resource: Resource is an ObjectRef to another Kubernetes resource in the \
        namespace of the Ingress object. If resource is specified, serviceName and \
        servicePort must not be specified.
    """

    def __init__(
        self,
        service_name: str,
        service_port: int,
        resource: Optional[TypedLocalObjectReference] = None,
    ):
        self.resource = resource
        self.serviceName = service_name
        self.servicePort = service_port


class HTTPIngressPath(HelmYaml):
    """
    :param backend: Backend defines the referenced service endpoint to which the \
        traffic will be forwarded to.
    :param path: Path is matched against the path of an incoming request. Currently it \
        can contain characters disallowed from the conventional "path" part of a URL \
        as defined by RFC 3986. Paths must begin with a '/'. When unspecified, all \
        paths from incoming requests are matched.
    :param path_type: PathType determines the interpretation of the Path matching. \
        PathType can be one of the following values: * Exact: Matches the URL path \
        exactly. * Prefix: Matches based on a URL path prefix split by '/'. Matching \
        is   done on a path element by element basis. A path element refers is the   \
        list of labels in the path split by the '/' separator. A request is a   match \
        for path p if every p is an element-wise prefix of p of the   request path. \
        Note that if the last element of the path is a substring   of the last element \
        in request path, it is not a match (e.g. /foo/bar   matches /foo/bar/baz, but \
        does not match /foo/barbaz). * ImplementationSpecific: Interpretation of the \
        Path matching is up to   the IngressClass. Implementations can treat this as a \
        separate PathType   or treat it identically to Prefix or Exact path types. \
        Implementations are required to support all path types. Defaults to \
        ImplementationSpecific.
    """

    def __init__(
        self,
        backend: IngressBackend,
        path: Optional[str] = None,
        path_type: Optional[str] = None,
    ):
        self.backend = backend
        self.path = path
        self.pathType = path_type


class HTTPIngressRuleValue(HelmYaml):
    """
    :param paths: A collection of paths that map requests to backends.
    """

    def __init__(self, paths: List[HTTPIngressPath]):
        self.paths = paths


class IngressRule(HelmYaml):
    """
    :param http: None
    :param host: Host is the fully qualified domain name of a network host, as defined \
        by RFC 3986. Note the following deviations from the "host" part of the URI as \
        defined in RFC 3986: 1. IPs are not allowed. Currently an IngressRuleValue can \
        only apply to    the IP in the Spec of the parent Ingress. 2. The `:` \
        delimiter is not respected because ports are not allowed.       Currently the \
        port of an Ingress is implicitly :80 for http and       :443 for https. Both \
        these may change in the future. Incoming requests are matched against the host \
        before the IngressRuleValue. If the host is unspecified, the Ingress routes \
        all traffic based on the specified IngressRuleValue.  Host can be "precise" \
        which is a domain name without the terminating dot of a network host (e.g. \
        "foo.bar.com") or "wildcard", which is a domain name prefixed with a single \
        wildcard label (e.g. "*.foo.com"). The wildcard character '\\*' must appear by \
        itself as the first DNS label and matches only a single label. You cannot have \
        a wildcard label by itself (e.g. Host == "*"). Requests will be matched \
        against the Host field in the following way: 1. If Host is precise, the \
        request matches this rule if the http host header is equal to Host. 2. If Host \
        is a wildcard, then the request matches this rule if the http host header is \
        to equal to the suffix (removing the first label) of the wildcard rule.
    """

    def __init__(self, http: HTTPIngressRuleValue, host: Optional[str] = None):
        self.host = host
        self.http = http


class IngressSpec(HelmYaml):
    """
    :param ingress_class_name: IngressClassName is the name of the IngressClass cluster \
        resource. The associated IngressClass defines which controller will implement \
        the resource. This replaces the deprecated `kubernetes.io/ingress.class` \
        annotation. For backwards compatibility, when that annotation is set, it must \
        be given precedence over this field. The controller may emit a warning if the \
        field and annotation have different values. Implementations of this API should \
        ignore Ingresses without a class specified. An IngressClass resource may be \
        marked as default, which can be used to set a default value for this field. \
        For more information, refer to the IngressClass documentation.
    :param backend: A default backend capable of servicing requests that don't match \
        any rule. At least one of 'backend' or 'rules' must be specified. This field \
        is optional to allow the loadbalancer controller or defaulting logic to \
        specify a global default.
    :param rules: A list of host rules used to configure the Ingress. If unspecified, \
        or no rule matches, all traffic is sent to the default backend.
    :param tls: TLS configuration. Currently the Ingress only supports a single TLS \
        port, 443. If multiple members of this list specify different hosts, they will \
        be multiplexed on the same port according to the hostname specified through \
        the SNI TLS extension, if the ingress controller fulfilling the ingress \
        supports SNI.
    """

    def __init__(
        self,
        ingress_class_name: Optional[str] = None,
        backend: Optional[IngressBackend] = None,
        rules: Optional[List[IngressRule]] = None,
        tls: Optional[List[IngressTLS]] = None,
    ):
        self.ingressClassName = ingress_class_name
        self.backend = backend
        self.rules = rules
        self.tls = tls


class Ingress(Extensions):
    """
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: Spec is the desired state of the Ingress. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    _non_standard_version = "v1beta1"

    def __init__(
        self, metadata: ObjectMeta, spec: IngressSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec
