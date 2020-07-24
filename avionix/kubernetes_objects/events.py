from datetime import time

from avionix.yaml.yaml_handling import HelmYaml


class EventSeries(HelmYaml):
    """
    :param count:Number of occurrences in this series up to the last heartbeat time
    :type count: int
    :param last_observed_time:Time when last Event from the series was seen before \
        last heartbeat.
    :type last_observed_time: time
    :param state:Information whether this series is ongoing or finished. Deprecated. \
        Planned removal for 1.18
    :type state: str
    """

    def __init__(self, count: int, last_observed_time: time, state: str):
        self.count = count
        self.lastObservedTime = last_observed_time
        self.state = state
