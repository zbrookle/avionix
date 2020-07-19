import logging
from pathlib import Path

import pytest

from avionix import ChartInfo
from avionix.tests.utils import get_test_deployment

logging.basicConfig(format="[%(filename)s: %(lineno)s] %(message)s", level=logging.INFO)


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
    return Path(__file__).parent
