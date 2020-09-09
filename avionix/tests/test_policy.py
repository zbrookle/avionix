from typing import List, Optional, Union

import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.errors import HelmError
from avionix.kube.core import SELinuxOptions
from avionix.kube.policy import (
    AllowedCSIDriver,
    AllowedFlexVolume,
    AllowedHostPath,
    Eviction,
    FSGroupStrategyOptions,
    HostPortRange,
    IDRange,
    PodDisruptionBudget,
    PodDisruptionBudgetSpec,
    PodSecurityPolicy,
    PodSecurityPolicySpec,
    RunAsGroupStrategyOptions,
    RunAsUserStrategyOptions,
    RuntimeClassStrategyOptions,
    SELinuxStrategyOptions,
    SupplementalGroupsStrategyOptions,
)
from avionix.testing.helpers import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


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


def get_base_pod_security_policy(
    name: str,
    allowed_csi_drivers: Optional[List[AllowedCSIDriver]] = None,
    allowed_flex_volumes: Optional[List[AllowedFlexVolume]] = None,
    allowed_host_paths: Optional[List[AllowedHostPath]] = None,
    host_ports: Optional[List[HostPortRange]] = None,
    run_as_group: Optional[RunAsGroupStrategyOptions] = None,
    runtime_class: Optional[RuntimeClassStrategyOptions] = None,
    se_linux_options: Optional[SELinuxOptions] = None,
):
    return PodSecurityPolicy(
        ObjectMeta(name=name),
        PodSecurityPolicySpec(
            FSGroupStrategyOptions("RunAsAny"),
            RunAsUserStrategyOptions("RunAsAny"),
            SELinuxStrategyOptions("RunAsAny", se_linux_options),
            SupplementalGroupsStrategyOptions("RunAsAny"),
            allowed_csidrivers=allowed_csi_drivers,
            allowed_flex_volumes=allowed_flex_volumes,
            allowed_host_paths=allowed_host_paths,
            host_ports=host_ports,
            run_as_group=run_as_group,
            runtime_class=runtime_class,
        ),
    )


@pytest.mark.parametrize(
    "pod_security_policy",
    [
        get_base_pod_security_policy("minimal-test-pod-security"),
        get_base_pod_security_policy(
            "csi-driver-security", allowed_csi_drivers=[AllowedCSIDriver("driver-name")]
        ),
        get_base_pod_security_policy(
            "flex-volume-security",
            allowed_flex_volumes=[AllowedFlexVolume("driver-name")],
        ),
        get_base_pod_security_policy(
            "host-path-security", allowed_host_paths=[AllowedHostPath("/tmp")]
        ),
        get_base_pod_security_policy(
            "group-security", run_as_group=RunAsGroupStrategyOptions("RunAsAny"),
        ),
        get_base_pod_security_policy(
            "runtime-class-security",
            runtime_class=RuntimeClassStrategyOptions(["test-class"]),
        ),
        get_base_pod_security_policy(
            "group-id-range-security",
            run_as_group=RunAsGroupStrategyOptions(
                ranges=[IDRange(1, 2)], rule="MustRunAs"
            ),
        ),
        get_base_pod_security_policy(
            "se-linux-options", se_linux_options=SELinuxOptions("None")
        ),
        get_base_pod_security_policy(
            "host-port-range", host_ports=[HostPortRange(4, 1)]
        ),
    ],
)
def test_pod_security_policy(chart_info, pod_security_policy: PodSecurityPolicy):
    builder = ChartBuilder(chart_info, [pod_security_policy],)
    with ChartInstallationContext(builder):
        pod_security_policy_info = kubectl_get("podsecuritypolicy")
        assert pod_security_policy_info["NAME"][0] == pod_security_policy.metadata.name
        assert (
            pod_security_policy_info["SELINUX"][0]
            == pod_security_policy.spec.seLinux.rule
        )
        assert (
            pod_security_policy_info["RUNASUSER"][0]
            == pod_security_policy.spec.runAsUser.rule
        )
        assert (
            pod_security_policy_info["FSGROUP"][0]
            == pod_security_policy.spec.fsGroup.rule
        )
