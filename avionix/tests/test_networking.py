from typing import List, Optional

import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.meta import LabelSelector
from avionix.kube.networking import (
    IPBlock,
    NetworkPolicy,
    NetworkPolicyEgressRule,
    NetworkPolicyIngressRule,
    NetworkPolicyPeer,
    NetworkPolicyPort,
    NetworkPolicySpec,
    IngressClass,
    IngressClassSpec,
)
from avionix.testing.helpers import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext

SELECTOR = LabelSelector({"test": "test"})
POLICY_PORT = NetworkPolicyPort(80, "TCP")
POLICY_PEER = NetworkPolicyPeer(IPBlock("10.0.0.0/24"))


@pytest.mark.parametrize(
    "name,selector,egress,ingress, policy_types",
    [
        ("empty-policy", None, None, None, None),
        ("with-selector", SELECTOR, None, None, None),
        (
            "egress",
            SELECTOR,
            [NetworkPolicyEgressRule([POLICY_PORT], [POLICY_PEER],)],
            None,
            None,
        ),
        (
            "ingress",
            SELECTOR,
            None,
            [NetworkPolicyIngressRule([POLICY_PEER], [POLICY_PORT])],
            None,
        ),
        ("policy-types", SELECTOR, None, None, ["Ingress"]),
    ],
)
def test_network_policy(
    chart_info,
    name: str,
    selector: Optional[LabelSelector],
    egress: Optional[List[NetworkPolicyEgressRule]],
    ingress: Optional[List[NetworkPolicyIngressRule]],
    policy_types: Optional[List[str]],
):
    builder = ChartBuilder(
        chart_info,
        [
            NetworkPolicy(
                ObjectMeta(name=name),
                NetworkPolicySpec(egress, ingress, selector, policy_types),
            )
        ],
    )
    with ChartInstallationContext(builder):
        network_policy_info = kubectl_get("networkpolicy")
        assert network_policy_info["NAME"][0] == name
        if selector is None:
            selector = "<none>"
        if isinstance(selector, LabelSelector):
            match_labels = selector.matchLabels
            first_key = list(match_labels.keys())[0]
            selector = f"{first_key}={match_labels[first_key]}"
        assert network_policy_info["POD-SELECTOR"][0] == selector


def test_ingress_class(chart_info):
    ingress_class = IngressClass(
        ObjectMeta(name="test-ingress-class"), IngressClassSpec("acme.io/foo")
    )
    builder = ChartBuilder(chart_info, [ingress_class],)
    with ChartInstallationContext(builder):
        ingress_class_info = kubectl_get("ingressclass")
        assert ingress_class_info["NAME"][0] == ingress_class.metadata.name
        assert ingress_class_info["CONTROLLER"][0] == ingress_class.spec.controller
