import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kubernetes_objects.rbac_authorization import PolicyRule, Role
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.fixture
def role():
    return Role(
        ObjectMeta(name="test-role"), [PolicyRule()]
    )


def test_role(chart_info, role):
    builder = ChartBuilder(chart_info, [role])
    with ChartInstallationContext(builder):
        roles = kubectl_get("roles", wide=True)
        assert roles["NAME"][0] == "test-role"
