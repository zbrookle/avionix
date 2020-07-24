from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.meta import ListMeta, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class CertificateSigningRequestCondition(HelmYaml):
    """
    :param last_update_time:timestamp for the last update to this condition
    :type last_update_time: time
    :param message:human readable message with details about the request state
    :type message: str
    :param reason:brief reason for the request state
    :type reason: str
    :param type:request approval state, currently Approved or Denied.
    :type type: str
    """

    def __init__(self, last_update_time: time, message: str, reason: str, type: str):
        self.lastUpdateTime = last_update_time
        self.message = message
        self.reason = reason
        self.type = type


class CertificateSigningRequestSpec(HelmYaml):
    """
    :param extra:Extra information about the requesting user. See user.Info interface \
        for details.
    :type extra: dict
    :param groups:Group information about the requesting user. See user.Info interface \
        for details.
    :type groups: List[str]
    :param request:Base64-encoded PKCS#10 CSR data
    :type request: str
    :param signer_name:Requested signer for the request. It is a qualified name in the \
        form: `scope-hostname.io/name`. If empty, it will be defaulted:  1. If it's a \
        kubelet client certificate, it is assigned     \
        "kubernetes.io/kube-apiserver-client-kubelet".  2. If it's a kubelet serving \
        certificate, it is assigned     "kubernetes.io/kubelet-serving".  3. \
        Otherwise, it is assigned "kubernetes.io/legacy-unknown". Distribution of \
        trust for signers happens out of band. You can select on this field using \
        `spec.signerName`.
    :type signer_name: str
    :param uid:UID information about the requesting user. See user.Info interface for \
        details.
    :type uid: str
    :param usages:allowedUsages specifies a set of usage contexts the key will be \
        valid for. See: https://tools.ietf.org/html/rfc5280#section-4.2.1.3      \
        https://tools.ietf.org/html/rfc5280#section-4.2.1.12
    :type usages: List[str]
    :param username:Information about the requesting user. See user.Info interface for \
        details.
    :type username: str
    """

    def __init__(
        self,
        extra: dict,
        groups: List[str],
        request: str,
        signer_name: str,
        uid: str,
        usages: List[str],
        username: str,
    ):
        self.extra = extra
        self.groups = groups
        self.request = request
        self.signerName = signer_name
        self.uid = uid
        self.usages = usages
        self.username = username


class CertificateSigningRequest(KubernetesBaseObject):
    """
    :param metadata:None
    :type metadata: ObjectMeta
    :param spec:The certificate request itself and any additional information.
    :type spec: CertificateSigningRequestSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self,
        metadata: ObjectMeta,
        spec: CertificateSigningRequestSpec,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class CertificateSigningRequestList(KubernetesBaseObject):
    """
    :param items:None
    :type items: List[CertificateSigningRequest]
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
        items: List[CertificateSigningRequest],
        metadata: ListMeta,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
