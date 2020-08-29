import logging

import pandas
import pytest

from avionix import ChartDependency, ChartInfo, ObjectMeta
from avionix.kube.core import (
    ConfigMap,
    HostPathVolumeSource,
    PersistentVolumeSpec,
    Pod,
    PodSpec,
    PodTemplateSpec,
    ServiceAccount,
)
from avionix.kube.meta import LabelSelector
from avionix.kube.reference import ObjectReference
from avionix.tests.utils import get_test_container, get_test_deployment

logging.basicConfig(format="[%(filename)s:%(lineno)s] %(message)s", level=logging.INFO)

pandas.set_option("display.max_columns", 50)


@pytest.fixture
def test_deployment1():
    return get_test_deployment(1)


@pytest.fixture
def test_deployment2():
    return get_test_deployment(2)


@pytest.fixture
def chart_info():
    return ChartInfo(
        api_version="3.2.4", name="test", version="0.1.0", app_version="v1",
    )


@pytest.fixture
def pod_spec():
    return PodSpec([get_test_container(0)])


@pytest.fixture
def pod(pod_spec):
    return Pod(ObjectMeta(name="test-pod"), spec=pod_spec)


@pytest.fixture
def test_labels():
    return {"type": "master"}


@pytest.fixture
def pod_template_spec(pod_spec, test_labels):
    return PodTemplateSpec(ObjectMeta(labels=test_labels), pod_spec)


@pytest.fixture
def selector(test_labels):
    return LabelSelector(match_labels=test_labels)


@pytest.fixture
def object_meta_event():
    return ObjectMeta(name="test-event")


@pytest.fixture
def event_obj_ref():
    return ObjectReference("test-pod", name="test-ref")


@pytest.fixture
def empty_service_account():
    return ServiceAccount(ObjectMeta(name="test-service-account"))


@pytest.fixture
def config_map():
    return ConfigMap(ObjectMeta(name="test-config-map"), data={"my_test_value": "yes"})


@pytest.fixture
def config_map2():
    return ConfigMap(
        ObjectMeta(name="test-config-map-2"), data={"my_test_value": "yes"}
    )


@pytest.fixture
def dependency():
    return ChartDependency(
        "grafana",
        "5.5.2",
        "https://kubernetes-charts.storage.googleapis.com/",
        "stable",
        values={"resources": {"requests": {"memory": "100Mi"}}},
    )


@pytest.fixture
def access_modes():
    return ["ReadWriteMany"]


@pytest.fixture
def persistent_volume_spec(access_modes):
    return PersistentVolumeSpec(
        access_modes,
        capacity={"storage": 1},
        host_path=HostPathVolumeSource("/home/test/tmp"),
        storage_class_name="standard",
    )
