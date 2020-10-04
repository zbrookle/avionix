import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.extensions import (
    HTTPIngressPath,
    HTTPIngressRuleValue,
    Ingress,
    IngressBackend,
    IngressRule,
    IngressSpec,
    IngressTLS,
)
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.mark.parametrize(
    "ingress_spec",
    [
        IngressSpec(
            "ingress-class", backend=IngressBackend("test-service-string", "service")
        ),
        IngressSpec("ingress-class", backend=IngressBackend("test-service", 1)),
        IngressSpec(
            rules=[
                IngressRule(
                    HTTPIngressRuleValue(
                        [HTTPIngressPath(IngressBackend("test-service", 1))]
                    ),
                )
            ],
        ),
        IngressSpec(
            backend=IngressBackend("test-service", 1), tls=[IngressTLS("test")]
        ),
    ],
)
def test_ingress(chart_info, ingress_spec: IngressSpec):
    ingress = Ingress(ObjectMeta(name="test-ingress"), ingress_spec)
    builder = ChartBuilder(chart_info, [ingress])
    with ChartInstallationContext(builder):
        ingress_info = kubectl_get("ingress")
        print(ingress_info)
        assert ingress_info["NAME"][0] == ingress.metadata.name
        assert (
            ingress_info["CLASS"][0] == ingress.spec.ingressClassName
            if ingress.spec.ingressClassName
            else "<none>"
        )
        assert ingress_info["HOSTS"][0] == "*"
        assert ingress_info["PORTS"][0] == "80" if not ingress.spec.tls else "80, 443"
