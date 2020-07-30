import logging

import pandas
import pytest

from avionix import ChartInfo, ObjectMeta
from avionix.kubernetes_objects.core import (
    Pod,
    PodSpec,
    PodTemplateSpec,
    ServiceAccount,
)
from avionix.kubernetes_objects.meta import LabelSelector
from avionix.kubernetes_objects.reference import ObjectReference
from avionix.tests.utils import get_test_container, get_test_deployment

logging.basicConfig(format="[%(filename)s: %(lineno)s] %(message)s", level=logging.INFO)

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
        api_version="3.2.4", name="test", version="0.1.0", app_version="v1"
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
