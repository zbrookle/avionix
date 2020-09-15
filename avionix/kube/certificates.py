"""
Contains CertificateSigningRequest class
"""

from typing import List, Optional

from avionix.kube.base_objects import Certificates
from avionix.kube.meta import ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class CertificateSigningRequestSpec(HelmYaml):
    """
    :param request: Base64-encoded PKCS#10 CSR data
    :param signer_name: Requested signer for the request. It is a qualified name in the \
        form: `scope-hostname.io/name`. If empty, it will be defaulted:  1. If it's a \
        kubelet client certificate, it is assigned     \
        "kubernetes.io/kube-apiserver-client-kubelet".  2. If it's a kubelet serving \
        certificate, it is assigned     "kubernetes.io/kubelet-serving".  3. \
        Otherwise, it is assigned "kubernetes.io/legacy-unknown". Distribution of \
        trust for signers happens out of band. You can select on this field using \
        `spec.signerName`.
    :param usages: allowedUsages specifies a set of usage contexts the key will be \
        valid for. See: https://tools.ietf.org/html/rfc5280#section-4.2.1.3      \
        https://tools.ietf.org/html/rfc5280#section-4.2.1.12
    """

    def __init__(
        self,
        request: str,
        signer_name: Optional[str] = None,
        usages: Optional[List[str]] = None,
    ):
        self.request = request
        self.signerName = signer_name
        self.usages = usages


class CertificateSigningRequest(Certificates):
    """
    :param metadata: None
    :param spec: The certificate request itself and any additional information.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    _non_standard_version = "v1beta1"

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: CertificateSigningRequestSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec
