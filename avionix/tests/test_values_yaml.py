import re

import pytest
import yaml

from avionix import ChartBuilder, ChartInfo, ObjectMeta, Value, Values
from avionix._process_utils import custom_check_output
from avionix.kube.core import ConfigMap
from avionix.testing.installation_context import ChartInstallationContext


@pytest.fixture
def config_map_value_yaml():
    return ConfigMap(
        ObjectMeta(name="test-values"),
        {"my_value": Value("my_value"), "my_nested_value": Value("my.nested.value")},
    )


@pytest.fixture
def values_yaml():
    return Values({"my_value": "some_value", "my": {"nested": {"value": 0}}})


def test_values_yaml_output(chart_info: ChartInfo, config_map_value_yaml, values_yaml):
    template_directory = ChartBuilder(
        chart_info, [config_map_value_yaml], values=values_yaml,
    ).generate_chart()

    with open(template_directory / "ConfigMap-0.yaml") as config_map_file:
        assert (
            config_map_file.read()
            == """apiVersion: v1
data:
  my_nested_value: '{{ .Values.my.nested.value }}'
  my_value: '{{ .Values.my_value }}'
kind: ConfigMap
metadata:
  name: test-values
"""
        )

    with open(template_directory.parent / "values.yaml") as values_file:
        assert (
            values_file.read()
            == """my:
  nested:
    value: 0
my_value: some_value
"""
        )


def get_config_map_data():
    output = custom_check_output("kubectl describe configmap")
    match = re.match(r".*Data\n====\n(?P<data>.*)Events:.*", output, re.DOTALL)
    if not match:
        raise Exception("Match must exist to get config map data!")
    data_string = match.group("data").replace("----\n", "").replace(":\n", ": ")
    data = yaml.safe_load(data_string)
    return data


def test_values_yaml_build(chart_info: ChartInfo, config_map_value_yaml, values_yaml):
    builder = ChartBuilder(chart_info, [config_map_value_yaml], values=values_yaml,)
    with ChartInstallationContext(builder):
        assert get_config_map_data() == {"my_nested_value": 0, "my_value": "some_value"}


def test_values_yaml_with_dependencies(
    config_map_value_yaml, values_yaml, dependency_chart_info
):
    builder = ChartBuilder(
        dependency_chart_info, [config_map_value_yaml], values=values_yaml
    )
    with ChartInstallationContext(builder):
        assert get_config_map_data() == {"my_nested_value": 0, "my_value": "some_value"}
        assert builder.is_installed
