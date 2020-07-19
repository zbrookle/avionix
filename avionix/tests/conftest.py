import logging

import pytest

from avionix.tests.utils import get_test_deployment

logging.basicConfig(format="[%(filename)s: %(lineno)s] %(message)s", level=logging.INFO)


@pytest.fixture
def test_deployment1():
    return get_test_deployment(1)


@pytest.fixture
def test_deployment2():
    return get_test_deployment(2)
