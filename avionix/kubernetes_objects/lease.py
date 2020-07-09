from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.metadata import ListMeta, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class LeaseSpec(HelmYaml):
    """
    :param acquire_time:acquireTime is a time when the current lease was acquired.
    :type acquire_time: time
    :param holder_identity:holderIdentity contains the identity of the holder of a \
        current lease.
    :type holder_identity: str
    :param lease_duration_seconds:leaseDurationSeconds is a duration that candidates \
        for a lease need to wait to force acquire it. This is measure against time of \
        last observed RenewTime.
    :type lease_duration_seconds: int
    :param lease_transitions:leaseTransitions is the number of transitions of a lease \
        between holders.
    :type lease_transitions: int
    :param renew_time:renewTime is a time when the current holder of a lease has last \
        updated the lease.
    :type renew_time: time
    """

    def __init__(
        self,
        acquire_time: time,
        holder_identity: str,
        lease_duration_seconds: int,
        lease_transitions: int,
        renew_time: time,
    ):
        self.acquireTime = acquire_time
        self.holderIdentity = holder_identity
        self.leaseDurationSeconds = lease_duration_seconds
        self.leaseTransitions = lease_transitions
        self.renewTime = renew_time


class Lease(KubernetesBaseObject):
    """
    :param metadata:More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the Lease. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: LeaseSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: LeaseSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class LeaseList(KubernetesBaseObject):
    """
    :param items:Items is a list of schema objects.
    :type items: List[Lease]
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, items: List[Lease], metadata: ListMeta, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
