from avionix.kube.authentication import (
    TokenReview,
    TokenReviewSpec,
    TokenRequest,
    TokenRequestSpec,
)
from avionix.testing.installation_context import ChartInstallationContext
from avionix.testing.helpers import kubectl_get, KubectGetException
from avionix import ChartBuilder, ObjectMeta
import pytest
from avionix.errors import HelmError


@pytest.mark.xfail(
    raises=KubectGetException, reason="Cannot use kubectl get on " "tokenreview"
)
def test_token_review(chart_info):
    builder = ChartBuilder(
        chart_info,
        [
            TokenReview(
                ObjectMeta(name="test-token"),
                TokenReviewSpec(["audience", "other_auditence"], "tokentoken"),
            )
        ],
    )
    with ChartInstallationContext(builder):
        token_review_info = kubectl_get("tokenreview")
        print(token_review_info)
        assert token_review_info["NAME"][0] == "test_name"
        assert token_review_info["DESIRED"][0] == "1"
        assert token_review_info["CURRENT"][0] == "1"


@pytest.mark.xfail(raises=HelmError, reason="Helm does not support token request")
def test_token_request(chart_info):
    builder = ChartBuilder(
        chart_info,
        [
            TokenRequest(
                ObjectMeta(name="token-request"),
                TokenRequestSpec(["audience1", "audience2"], None, None),
            )
        ],
    )
    with ChartInstallationContext(builder):
        print(kubectl_get("tokenrequest"))
