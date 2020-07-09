from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.yaml.yaml_handling import HelmYaml


class Preconditions(HelmYaml):
    """
    :param resource_version:Specifies the target ResourceVersion
    :type resource_version: str
    :param uid:Specifies the target UID.
    :type uid: str
    """

    def __init__(self, resource_version: str, uid: str):
        self.resourceVersion = resource_version
        self.uid = uid


class DeleteOptions(KubernetesBaseObject):
    """
    :param dry_run:When present, indicates that modifications should not be persisted. \
        An invalid or unrecognized dryRun directive will result in an error response \
        and no further processing of the request. Valid values are: - All: all dry run \
        stages will be processed
    :type dry_run: List[str]
    :param orphan_dependents:Deprecated: please use the PropagationPolicy, this field \
        will be deprecated in 1.7. Should the dependent objects be orphaned. If \
        true/false, the "orphan" finalizer will be added to/removed from the object's \
        finalizers list. Either this field or PropagationPolicy may be set, but not \
        both.
    :type orphan_dependents: bool
    :param preconditions:Must be fulfilled before a deletion is carried out. If not \
        possible, a 409 Conflict status will be returned.
    :type preconditions: Preconditions
    :param propagation_policy:Whether and how garbage collection will be performed. \
        Either this field or OrphanDependents may be set, but not both. The default \
        policy is decided by the existing finalizer set in the metadata.finalizers and \
        the resource-specific default policy. Acceptable values are: 'Orphan' - orphan \
        the dependents; 'Background' - allow the garbage collector to delete the \
        dependents in the background; 'Foreground' - a cascading policy that deletes \
        all dependents in the foreground.
    :type propagation_policy: str
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    :param grace_period_seconds:The duration in seconds before the object should be \
        deleted. Value must be non-negative integer. The value zero indicates delete \
        immediately. If this value is nil, the default grace period for the specified \
        type will be used. Defaults to a per object value if not specified. zero means \
        delete immediately.
    :type grace_period_seconds: Optional[int]
    """

    def __init__(
        self,
        dry_run: List[str],
        orphan_dependents: bool,
        preconditions: Preconditions,
        propagation_policy: str,
        api_version: Optional[str] = None,
        grace_period_seconds: Optional[int] = None,
    ):
        super().__init__(api_version)
        self.dryRun = dry_run
        self.orphanDependents = orphan_dependents
        self.preconditions = preconditions
        self.propagationPolicy = propagation_policy
        self.gracePeriodSeconds = grace_period_seconds
