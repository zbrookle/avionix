import logging
from pathlib import Path

import pandas
import pytest

from avionix import ChartInfo, ObjectMeta
from avionix.kubernetes_objects.pod import Pod, PodSpec, PodTemplateSpec
from avionix.tests.utils import get_test_container, get_test_deployment
import os
import shutil

logging.basicConfig(format="[%(filename)s: %(lineno)s] %(message)s", level=logging.INFO)

pandas.set_option("display.max_columns", 50)


@pytest.fixture(scope="function", autouse=True)
def setup_environment(test_folder):
    os.makedirs(test_folder, exist_ok=True)
    yield
    if os.path.exists(test_folder):
        shutil.rmtree(test_folder)


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


@pytest.fixture(scope="module")
def test_folder():
    return Path.cwd() / "tmp"


@pytest.fixture
def pod_spec():
    return PodSpec([get_test_container(0)])


@pytest.fixture
def pod(pod_spec):
    return Pod(ObjectMeta(name="test-pod"), spec=pod_spec)


@pytest.fixture
def pod_template_spec(pod_spec):
    return PodTemplateSpec(ObjectMeta(labels={"type": "master"}), pod_spec)
