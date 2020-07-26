import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.extensions import (
    HTTPIngressPath,
    HTTPIngressRuleValue,
    Ingress,
    IngressBackend,
    IngressRule,
    IngressSpec,
)
from avionix.testing import ChartInstallationContext, kubectl_get


@pytest.fixture
def ingress_backend():
    return IngressBackend("test-service", 1)


@pytest.fixture
def ingress_w_rules(ingress_backend):
    return Ingress(
        ObjectMeta(name="test-ingress"),
        IngressSpec(
            "ingress-class",
            rules=[
                IngressRule(
                    "me.com", HTTPIngressRuleValue([HTTPIngressPath(ingress_backend)]),
                )
            ],
        ),
    )


@pytest.fixture
def ingress_w_backend(ingress_backend):
    return Ingress(
        ObjectMeta(name="test-ingress"),
        IngressSpec("ingress-class", backend=ingress_backend),
    )


def test_ingress_w_rules(chart_info, ingress_w_rules):
    builder = ChartBuilder(chart_info, [ingress_w_rules])
    with ChartInstallationContext(builder):
        ingress_info = kubectl_get("ingress")
        assert ingress_info["NAME"][0] == "test-ingress"
        assert ingress_info["CLASS"][0] == "ingress-class"
        assert ingress_info["HOSTS"][0] == "me.com"
        assert ingress_info["PORTS"][0] == "80"


def test_ingress_w_backend(chart_info, ingress_w_backend):
    builder = ChartBuilder(chart_info, [ingress_w_backend])
    with ChartInstallationContext(builder):
        ingress_info = kubectl_get("ingress")
        assert ingress_info["NAME"][0] == "test-ingress"
        assert ingress_info["CLASS"][0] == "ingress-class"
        assert ingress_info["HOSTS"][0] == "*"
        assert ingress_info["PORTS"][0] == "80"
