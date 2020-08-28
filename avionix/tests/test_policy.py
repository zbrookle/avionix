from avionix import ChartBuilder, ObjectMeta
from avionix.kube.policy import PodDisruptionBudget, PodDisruptionBudgetSpec, Eviction
from avionix.testing.helpers import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext
import pytest
from typing import Union
from avionix.errors import HelmError


def none_to_na(value: Union[str, int]):
    if value is None:
        return "N/A"
    return str(value)


@pytest.mark.parametrize(
    "pod_disruption_budget",
    [
        PodDisruptionBudget(ObjectMeta(name="test-budget"), PodDisruptionBudgetSpec(),),
        PodDisruptionBudget(
            ObjectMeta(name="test-budget-max"), PodDisruptionBudgetSpec("1%"),
        ),
        PodDisruptionBudget(
            ObjectMeta(name="test-budget-max"),
            PodDisruptionBudgetSpec(min_available=2),
        ),
    ],
)
def test_pod_disruption_budget(chart_info, pod_disruption_budget):
    builder = ChartBuilder(chart_info, [pod_disruption_budget],)
    with ChartInstallationContext(builder):
        budget_info = kubectl_get("poddisruptionbudget")
        assert budget_info["NAME"][0] == pod_disruption_budget.metadata.name
        assert budget_info["MIN AVAILABLE"][0] == none_to_na(
            pod_disruption_budget.spec.minAvailable
        )
        assert budget_info["MAX UNAVAILABLE"][0] == none_to_na(
            pod_disruption_budget.spec.maxUnavailable
        )


@pytest.mark.xfail(
    raises=HelmError, reason="Minikube version not high enough for eviction?"
)
def test_eviction(chart_info):
    builder = ChartBuilder(
        chart_info, [Eviction(ObjectMeta(name="test-eviction"), None)],
    )
    with ChartInstallationContext(builder):
        kubectl_get("eviction")
