from datetime import time
from typing import List, Optional

from helm_factory.kubernetes_objects.base_objects import KubernetesBaseObject
from helm_factory.kubernetes_objects.metadata import ListMeta, ObjectMeta
from helm_factory.kubernetes_objects.reference import ObjectReference
from helm_factory.yaml.yaml_handling import HelmYaml


class EventSeries(HelmYaml):
    """
    :param count: Number of occurrences in this series up to the last heartbeat time
    :param last_observed_time: Time of the last occurrence observed
    :param state: State of this Series: Ongoing or Finished Deprecated. Planned \
        removal for 1.18
    """

    def __init__(self, count: int, last_observed_time: time, state: str):
        self.count = count
        self.lastObservedTime = last_observed_time
        self.state = state


class EventSource(HelmYaml):
    """
    :param component: Component from which the event is generated.
    :param host: Node name on which the event is generated.
    """

    def __init__(self, component: str, host: str):
        self.component = component
        self.host = host


class Event(KubernetesBaseObject):
    """
    :param action: What action was taken/failed regarding to the Regarding object.
    :param count: The number of times this event has occurred.
    :param event_time: Time when this Event was first observed.
    :param first_timestamp: The time at which the event was first recorded. (Time of \
        server receipt is in TypeMeta.)
    :param involved_object: The object that this event is about.
    :param last_timestamp: The time at which the most recent occurrence of this event \
        was recorded.
    :param message: A human-readable description of the status of this operation.
    :param metadata: Standard object's metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    :param reason: This should be a short, machine understandable string that gives \
        the reason for the transition into the object's current status.
    :param related: Optional secondary object for more complex actions.
    :param reporting_component: Name of the controller that emitted this Event, e.g. \
        `kubernetes.io/kubelet`.
    :param reporting_instance: ID of the controller instance, e.g. `kubelet-xyzf`.
    :param series: Data about the Event series this event represents or nil if it's a \
        singleton Event.
    :param source: The component reporting this event. Should be a short machine \
        understandable string.
    :param type: Type of this event (Normal, Warning), new types could be added in the \
        future
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self,
        action: str,
        count: int,
        event_time: time,
        first_timestamp: time,
        involved_object: ObjectReference,
        last_timestamp: time,
        message: str,
        metadata: ObjectMeta,
        reason: str,
        related: ObjectReference,
        reporting_component: str,
        reporting_instance: str,
        series: EventSeries,
        source: EventSource,
        type: str,
        api_version: Optional[str] = None,
    ):
        super().__init__(api_version)
        self.action = action
        self.count = count
        self.eventTime = event_time
        self.firstTimestamp = first_timestamp
        self.involvedObject = involved_object
        self.lastTimestamp = last_timestamp
        self.message = message
        self.metadata = metadata
        self.reason = reason
        self.related = related
        self.reportingComponent = reporting_component
        self.reportingInstance = reporting_instance
        self.series = series
        self.source = source
        self.type = type


class WatchEvent(HelmYaml):
    """
    :param object: Object is:  * If Type is Added or Modified: the new state of the \
        object.  * If Type is Deleted: the state of the object immediately before \
        deletion.  * If Type is Error: *Status is recommended; other types may make \
        sense    depending on context.
    :param type: None
    """

    def __init__(self, object: str, type: str):
        self.object = object
        self.type = type


class EventList(KubernetesBaseObject):
    """
    :param items: List of events
    :param metadata: Standard list metadata. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    :param api_version: APIVersion defines the versioned schema of this representation \
        of an object. Servers should convert recognized schemas to the latest internal \
        value, and may reject unrecognized values. More info: \
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
    """

    def __init__(
        self, items: List[Event], metadata: ListMeta, api_version: Optional[str] = None
    ):
        super().__init__(api_version)
        self.items = items
        self.metadata = metadata
