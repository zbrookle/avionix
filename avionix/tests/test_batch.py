import pytest

from avionix import ChartBuilder, ObjectMeta
from avionix.kube.batch import CronJob, CronJobSpec, JobSpec, JobTemplateSpec
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext


@pytest.fixture
def cron_job(pod_template_spec):
    pod_template_spec.spec.restartPolicy = "Never"
    return CronJob(
        ObjectMeta(name="test-cron-job"),
        CronJobSpec(JobTemplateSpec(JobSpec(pod_template_spec)), "23 * * * 6",),
    )


def test_cron_job(chart_info, cron_job):
    builder = ChartBuilder(chart_info, [cron_job])
    with ChartInstallationContext(builder):
        cron_job_info = kubectl_get("cronjob")
        assert cron_job_info["NAME"][0] == "test-cron-job"
        assert cron_job_info["SCHEDULE"][0] == "23 * * * 6"
