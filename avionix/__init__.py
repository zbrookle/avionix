from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions

from avionix.chart_builder import ChartBuilder
from avionix.chart_info import ChartInfo
from avionix.chart_dependency import ChartDependency
