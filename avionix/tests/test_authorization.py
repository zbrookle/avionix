# from avionix.kube.authorization import (
#     SelfSubjectAccessReview,
#     SelfSubjectRulesReview,
#     LocalSubjectAccessReview,
#     SubjectAccessReview,
#     SelfSubjectAccessReviewSpec,
#     SelfSubjectAccessReview,
#     LocalSubjectAccessReview,
#     SubjectAccessReviewSpec,
#     NonResourceAttributes,
#     ResourceAttributes,
# )
# from avionix.testing.installation_context import ChartInstallationContext
# from avionix.testing.helpers import kubectl_get, KubectGetException
# from avionix import ChartBuilder, ObjectMeta
# import pytest
# from avionix.errors import HelmError
#
#
# @pytest.fixture
# def access_review_meta():
#     return ObjectMeta(name="access-review", )
#
#
# def test_selfsubjectaccessreview(chart_info, access_review_meta):
#     builder = ChartBuilder(
#         chart_info,
#         [SelfSubjectAccessReview(access_review_meta, SelfSubjectAccessReviewSpec(
#             NonResourceAttributes("/test", "GET"), None))],
#     )
#     with ChartInstallationContext(builder):
#         print(kubectl_get("selfsubjectaccessreview"))
#         raise Exception
