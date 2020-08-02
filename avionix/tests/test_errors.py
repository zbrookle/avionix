import pytest
from avionix.errors import ChartAlreadyInstalledError
from avionix import ChartBuilder


def test_already_installed_error(chart_info, config_map):
    builder = ChartBuilder(
        chart_info,
        [config_map],
    )
    builder.install_chart()
    with pytest.raises(ChartAlreadyInstalledError):
        builder.install_chart()
    builder.uninstall_chart()