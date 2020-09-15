"""
Contains Lease class
"""

from datetime import time
from typing import Optional

from avionix.kube.base_objects import Coordination
from avionix.kube.meta import ObjectMeta
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
        acquire_time: Optional[time] = None,
        holder_identity: Optional[str] = None,
        lease_duration_seconds: Optional[int] = None,
        lease_transitions: Optional[int] = None,
        renew_time: Optional[time] = None,
    ):
        self.acquireTime = acquire_time
        self.holderIdentity = holder_identity
        self.leaseDurationSeconds = lease_duration_seconds
        self.leaseTransitions = lease_transitions
        self.renewTime = renew_time


class Lease(Coordination):
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
