from typing import List

from avionix.kubernetes_objects.selector import LabelSelector
from avionix.yaml.yaml_handling import HelmYaml


class TopologySpreadConstraint(HelmYaml):
    """
    :param label_selector:LabelSelector is used to find matching pods. Pods that match \
        this label selector are counted to determine the number of pods in their \
        corresponding topology domain.
    :type label_selector: LabelSelector
    :param max_skew:MaxSkew describes the degree to which pods may be unevenly \
        distributed. It's the maximum permitted difference between the number of \
        matching pods in any two topology domains of a given topology type. For \
        example, in a 3-zone cluster, MaxSkew is set to 1, and pods with the same \
        labelSelector spread as 1/1/0: | zone1 | zone2 | zone3 | |   P   |   P   |     \
          | - if MaxSkew is 1, incoming pod can only be scheduled to zone3 to become \
        1/1/1; scheduling it onto zone1(zone2) would make the ActualSkew(2-0) on \
        zone1(zone2) violate MaxSkew(1). - if MaxSkew is 2, incoming pod can be \
        scheduled onto any zone. It's a required field. Default value is 1 and 0 is \
        not allowed.
    :type max_skew: int
    :param topology_key:TopologyKey is the key of node labels. Nodes that have a label \
        with this key and identical values are considered to be in the same topology. \
        We consider each <key, value> as a "bucket", and try to put balanced number of \
        pods into each bucket. It's a required field.
    :type topology_key: str
    :param when_unsatisfiable:WhenUnsatisfiable indicates how to deal with a pod if it \
        doesn't satisfy the spread constraint. - DoNotSchedule (default) tells the \
        scheduler not to schedule it - ScheduleAnyway tells the scheduler to still \
        schedule it It's considered as "Unsatisfiable" if and only if placing incoming \
        pod on any topology violates "MaxSkew". For example, in a 3-zone cluster, \
        MaxSkew is set to 1, and pods with the same labelSelector spread as 3/1/1: | \
        zone1 | zone2 | zone3 | | P P P |   P   |   P   | If WhenUnsatisfiable is set \
        to DoNotSchedule, incoming pod can only be scheduled to zone2(zone3) to become \
        3/2/1(3/1/2) as ActualSkew(2-1) on zone2(zone3) satisfies MaxSkew(1). In other \
        words, the cluster can still be imbalanced, but scheduler won't make it *more* \
        imbalanced. It's a required field.
    :type when_unsatisfiable: str
    """

    def __init__(
        self,
        label_selector: LabelSelector,
        max_skew: int,
        topology_key: str,
        when_unsatisfiable: str,
    ):
        self.labelSelector = label_selector
        self.maxSkew = max_skew
        self.topologyKey = topology_key
        self.whenUnsatisfiable = when_unsatisfiable


class TopologySelectorLabelRequirement(HelmYaml):
    """
    :param key:The label key that the selector applies to.
    :type key: str
    :param values:An array of string values. One value must match the label to be \
        selected. Each entry in Values is ORed.
    :type values: List[str]
    """

    def __init__(self, key: str, values: List[str]):
        self.key = key
        self.values = values


class TopologySelectorTerm(HelmYaml):
    """
    :param match_label_expressions:A list of topology selector requirements by labels.
    :type match_label_expressions: List[TopologySelectorLabelRequirement]
    """

    def __init__(self, match_label_expressions: List[TopologySelectorLabelRequirement]):
        self.matchLabelExpressions = match_label_expressions
