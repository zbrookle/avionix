from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.base_objects import KubernetesBaseObject
from avionix.kubernetes_objects.core import PodTemplateSpec
from avionix.kubernetes_objects.meta import LabelSelector, ListMeta, ObjectMeta
from avionix.yaml.yaml_handling import HelmYaml


class JobSpec(HelmYaml):
    """
    :param template:Describes the pod that will be created when executing a job. More \
        info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/  # noqa
    :type template: PodTemplateSpec
    :param completions:Specifies the desired number of successfully finished pods the \
        job should be run with.  Setting to nil means that the success of any pod \
        signals the success of all pods, and allows parallelism to have any positive \
        value.  Setting to 1 means that parallelism is limited to 1 and the success of \
        that pod signals the success of the job. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/  # noqa
    :type completions: int
    :param manual_selector:manualSelector controls generation of pod labels and pod \
        selectors. Leave `manualSelector` unset unless you are certain what you are \
        doing. When false or unset, the system pick labels unique to this job and \
        appends those labels to the pod template.  When true, the user is responsible \
        for picking unique labels and specifying the selector.  Failure to pick a \
        unique label may cause this and other jobs to not function correctly.  \
        However, You may see `manualSelector=true` in jobs that were created with the \
        old `extensions/v1beta1` API. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/#specifying-your-own-pod-selector  # noqa
    :type manual_selector: bool
    :param parallelism:Specifies the maximum desired number of pods the job should run \
        at any given time. The actual number of pods running in steady state will be \
        less than this number when ((.spec.completions - .status.successful) < \
        .spec.parallelism), i.e. when the work left to do is less than max \
        parallelism. More info: \
        https://kubernetes.io/docs/concepts/workloads/controllers/jobs-run-to-completion/  # noqa
    :type parallelism: int
    :param selector:A label query over pods that should match the pod count. Normally, \
        the system sets this field for you. More info: \
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors  # noqa
    :type selector: LabelSelector
    :param ttl_seconds_after_finished:ttlSecondsAfterFinished limits the lifetime of a \
        Job that has finished execution (either Complete or Failed). If this field is \
        set, ttlSecondsAfterFinished after the Job finishes, it is eligible to be \
        automatically deleted. When the Job is being deleted, its lifecycle guarantees \
        (e.g. finalizers) will be honored. If this field is unset, the Job won't be \
        automatically deleted. If this field is set to zero, the Job becomes eligible \
        to be deleted immediately after it finishes. This field is alpha-level and is \
        only honored by servers that enable the TTLAfterFinished feature.
    :type ttl_seconds_after_finished: int
    :param active_deadline_seconds:Specifies the duration in seconds relative to the \
        startTime that the job may be active before the system tries to terminate it; \
        value must be positive integer
    :type active_deadline_seconds: Optional[int]
    :param backoff_limit:Specifies the number of retries before marking this job \
        failed. Defaults to 6
    :type backoff_limit: Optional[int]
    """

    def __init__(
        self,
        template: PodTemplateSpec,
        completions: int,
        manual_selector: bool,
        parallelism: int,
        selector: LabelSelector,
        ttl_seconds_after_finished: int,
        active_deadline_seconds: Optional[int] = None,
        backoff_limit: Optional[int] = None,
    ):
        self.template = template
        self.completions = completions
        self.manualSelector = manual_selector
        self.parallelism = parallelism
        self.selector = selector
        self.ttlSecondsAfterFinished = ttl_seconds_after_finished
        self.activeDeadlineSeconds = active_deadline_seconds
        self.backoffLimit = backoff_limit


class JobCondition(HelmYaml):
    """
    :param last_probe_time:Last time the condition was checked.
    :type last_probe_time: time
    :param last_transition_time:Last time the condition transit from one status to \
        another.
    :type last_transition_time: time
    :param message:Human readable message indicating details about last transition.
    :type message: str
    :param reason:(brief) reason for the condition's last transition.
    :type reason: str
    :param type:Type of job condition, Complete or Failed.
    :type type: str
    """

    def __init__(
        self,
        last_probe_time: time,
        last_transition_time: time,
        message: str,
        reason: str,
        type: str,
    ):
        self.lastProbeTime = last_probe_time
        self.lastTransitionTime = last_transition_time
        self.message = message
        self.reason = reason
        self.type = type


class Job(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the desired behavior of a job. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: JobSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ObjectMeta, spec: JobSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class JobList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param items:items is the list of Jobs.
    :type items: List[Job]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    def __init__(
        self, metadata: ListMeta, items: List[Job], api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items


class JobTemplateSpec(HelmYaml):
    """
    :param metadata:Standard object's metadata of the jobs created from this template. \
        More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the desired behavior of the job. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: JobSpec
    """

    def __init__(self, metadata: ObjectMeta, spec: JobSpec):
        self.metadata = metadata
        self.spec = spec


class CronJobSpec(HelmYaml):
    """
    :param concurrency_policy:Specifies how to treat concurrent executions of a Job. \
        Valid values are: - "Allow" (default): allows CronJobs to run concurrently; - \
        "Forbid": forbids concurrent runs, skipping next run if previous run hasn't \
        finished yet; - "Replace": cancels currently running job and replaces it with \
        a new one
    :type concurrency_policy: str
    :param job_template:Specifies the job that will be created when executing a \
        CronJob.
    :type job_template: JobTemplateSpec
    :param schedule:The schedule in Cron format, see \
        https://en.wikipedia.org/wiki/Cron.
    :type schedule: str
    :param starting_deadline_seconds:Optional deadline in seconds for starting the job \
        if it misses scheduled time for any reason.  Missed jobs executions will be \
        counted as failed ones.
    :type starting_deadline_seconds: int
    :param failed_jobs_history_limit:The number of failed finished jobs to retain. \
        This is a pointer to distinguish between explicit zero and not specified. \
        Defaults to 1.
    :type failed_jobs_history_limit: Optional[int]
    :param successful_jobs_history_limit:The number of successful finished jobs to \
        retain. This is a pointer to distinguish between explicit zero and not \
        specified. Defaults to 3.
    :type successful_jobs_history_limit: Optional[int]
    :param suspend:This flag tells the controller to suspend subsequent executions, it \
        does not apply to already started executions.  Defaults to false.
    :type suspend: Optional[bool]
    """

    def __init__(
        self,
        concurrency_policy: str,
        job_template: JobTemplateSpec,
        schedule: str,
        starting_deadline_seconds: int,
        failed_jobs_history_limit: Optional[int] = None,
        successful_jobs_history_limit: Optional[int] = None,
        suspend: Optional[bool] = None,
    ):
        self.concurrencyPolicy = concurrency_policy
        self.jobTemplate = job_template
        self.schedule = schedule
        self.startingDeadlineSeconds = starting_deadline_seconds
        self.failedJobsHistoryLimit = failed_jobs_history_limit
        self.successfulJobsHistoryLimit = successful_jobs_history_limit
        self.suspend = suspend


class CronJob(KubernetesBaseObject):
    """
    :param metadata:Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ObjectMeta
    :param spec:Specification of the desired behavior of a cron job, including the \
        schedule. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status  # noqa
    :type spec: CronJobSpec
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    _non_standard_version = "v1beta1"

    def __init__(
        self, metadata: ObjectMeta, spec: CronJobSpec, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.spec = spec


class CronJobList(KubernetesBaseObject):
    """
    :param metadata:Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata  # noqa
    :type metadata: ListMeta
    :param items:items is the list of CronJobs.
    :type items: List[CronJob]
    :param api_version:APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources  # noqa
    :type api_version: Optional[str]
    """

    _non_standard_version = "v1beta1"

    def __init__(
        self,
        metadata: ListMeta,
        items: List[CronJob],
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.metadata = metadata
        self.items = items
