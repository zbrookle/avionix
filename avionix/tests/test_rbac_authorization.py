import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.rbac_authorization import (
    PolicyRule,
    Role,
    RoleBinding,
    RoleRef,
    Subject,
)
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.fixture
def role():
    return Role(ObjectMeta(name="test-role"), [PolicyRule()])


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
