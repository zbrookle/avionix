import pytest
from avionix.errors import ChartAlreadyInstalledError, NamespaceDoesNotExist
from avionix import ChartBuilder


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
