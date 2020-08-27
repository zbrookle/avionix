import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.rbac_authorization import (
    PolicyRule,
    Role,
    RoleBinding,
    RoleRef,
    Subject,
    ClusterRole,
    ClusterRoleBinding,
    AggregationRule,
)
from avionix.kube.meta import LabelSelector
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext
from pandas import DataFrame


@pytest.fixture(
    params=[{}, {"resources": ["pods"], "verbs": ["get"], "api_groups": [""]}]
)
def role(request):
    return Role(ObjectMeta(name="test-role"), [PolicyRule(**request.param)])


def test_role(chart_info, role):
    builder = ChartBuilder(chart_info, [role])
    with ChartInstallationContext(builder):
        roles = kubectl_get("roles")
        assert roles["NAME"][0] == "test-role"


@pytest.fixture
def role_binding_no_subjects(role):
    return RoleBinding(
        ObjectMeta(name="test-role-binding"),
        RoleRef(role.metadata.name, "rbac.authorization.k8s.io", "Role"),
    )


def test_role_binding(chart_info, role, role_binding_no_subjects):
    builder = ChartBuilder(chart_info, [role, role_binding_no_subjects])
    with ChartInstallationContext(builder):
        bindings = kubectl_get("rolebinding")
        assert bindings["NAME"][0] == "test-role-binding"
        assert bindings["ROLE"][0] == "Role/test-role"


@pytest.fixture
def role_binding_to_service_account(role, empty_service_account):
    return RoleBinding(
        ObjectMeta(name="test-role-binding"),
        RoleRef(role.metadata.name, "rbac.authorization.k8s.io", "Role"),
        [Subject(empty_service_account.metadata.name, kind="ServiceAccount")],
    )


def test_role_binding_to_service_account(
    chart_info, role, role_binding_to_service_account, empty_service_account
):
    builder = ChartBuilder(
        chart_info, [role, role_binding_to_service_account, empty_service_account]
    )
    with ChartInstallationContext(builder):
        bindings = kubectl_get("rolebinding")
        assert bindings["NAME"][0] == "test-role-binding"
        assert bindings["ROLE"][0] == "Role/test-role"


CLUSTER_ROLE = ClusterRole(
    ObjectMeta(name="role-w-policu-rules"), rules=[PolicyRule([""], ["pods"], ["get"])],
)


@pytest.mark.parametrize(
    "cluster_role",
    [
        ClusterRole(ObjectMeta(name="cluster-role")),
        ClusterRole(
            ObjectMeta(name="cluster-role-w-aggregation"),
            AggregationRule([LabelSelector({"test": "test"})]),
        ),
        CLUSTER_ROLE,
    ],
)
def test_cluster_role(chart_info, cluster_role: ClusterRole):
    builder = ChartBuilder(chart_info, [cluster_role])
    with ChartInstallationContext(builder):
        cluster_role_info = kubectl_get("clusterrole")
        assert cluster_role.metadata.name in cluster_role_info["NAME"]


@pytest.fixture
def cluster_role_binding():
    return ClusterRoleBinding(
        ObjectMeta(name="test-role-binding"),
        RoleRef(CLUSTER_ROLE.metadata.name, "rbac.authorization.k8s.io", "ClusterRole"),
    )


def test_cluster_role_binding(chart_info, cluster_role_binding: ClusterRoleBinding):
    builder = ChartBuilder(chart_info, [cluster_role_binding, CLUSTER_ROLE])
    with ChartInstallationContext(builder):
        cluster_role_binding_info = kubectl_get("clusterrolebinding")
        info_frame = DataFrame(cluster_role_binding_info)
        info_frame = info_frame[
            info_frame["NAME"] == cluster_role_binding.metadata.name
        ].reset_index()
        assert info_frame["NAME"][0] == cluster_role_binding.metadata.name
        assert info_frame["ROLE"][0] == f"ClusterRole/{CLUSTER_ROLE.metadata.name}"
