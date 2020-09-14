from avionix import ChartBuilder, ChartInfo, ObjectMeta, Value, Values
from avionix.kube.core import ConfigMap

config_map = ConfigMap(
    ObjectMeta(name="test-values"),
    {"my_value": Value("my_value"), "my_nested_value": Value("my.nested.value")},
)
values = Values({"my_value": "some_value", "my": {"nested": {"value": 0}}})
chart = ChartBuilder(
    ChartInfo(
        api_version="3.2.4",
        name="values_yaml_example",
        version="0.1.0",
        app_version="v1",
    ),
    [],
    values=values,
)
