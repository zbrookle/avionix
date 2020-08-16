from datetime import time
from typing import List, Optional

from avionix.kube.base_objects import KubernetesBaseObject
from avionix.kube.meta import ListMeta, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class LeaseSpec(HelmYaml):
    """
    :param acquire_time: acquireTime is a time when the current lease was acquired.
    :param holder_identity: holderIdentity contains the identity of the holder of a \
        current lease.
    :param lease_duration_seconds: leaseDurationSeconds is a duration that candidates \
        for a lease need to wait to force acquire it. This is measure against time of \
        last observed RenewTime.
    :param lease_transitions: leaseTransitions is the number of transitions of a lease \
        between holders.
    :param renew_time: renewTime is a time when the current holder of a lease has last \
        updated the lease.
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
    :param metadata: More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param spec: Specification of the Lease. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self, metadata: ObjectMeta, spec: LeaseSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class LeaseList(KubernetesBaseObject):
    """
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :param items: Items is a list of schema objects.
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    """

    def __init__(
        self, metadata: ListMeta, items: List[Lease], api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items
