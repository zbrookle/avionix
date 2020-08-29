import pytest

from avionix import ChartBuilder
from avionix.errors import (
    ChartAlreadyInstalledError,
    ChartNotInstalledError,
    HelmError,
    NamespaceDoesNotExist,
)


def test_chart_not_installed_error(chart_info, config_map):
    builder = ChartBuilder(chart_info, [config_map])
    with pytest.raises(ChartNotInstalledError):
        builder.upgrade_chart()


def test_already_installed_error(chart_info, config_map):
    builder = ChartBuilder(chart_info, [config_map],)
    builder.install_chart()
    with pytest.raises(ChartAlreadyInstalledError):
        builder.install_chart()
    builder.uninstall_chart()


def test_namespace_doesnt_exist(chart_info):
    builder = ChartBuilder(chart_info, [], namespace="12345678")
    with pytest.raises(
        NamespaceDoesNotExist,
        match=".*To create namespace on installation, "
        "use create_namespace=True in the ChartBuilder class.*",
    ):
        builder.install_chart()


def test_raises_when_invalid_upgrade_parameter_passed(chart_info, config_map):
    builder = ChartBuilder(chart_info, [config_map])
    builder.install_chart()
    with pytest.raises(HelmError):
        builder.upgrade_chart(options={"my-invalid-option": "hello"})
