from pandas import DataFrame
import pytest

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kube.core import (
    Binding,
    ConfigMap,
    EndpointAddress,
    Endpoints,
    EndpointSubset,
    Event,
    ExecAction,
    HostPathVolumeSource,
    HTTPGetAction,
    LimitRange,
    LimitRangeItem,
    LimitRangeSpec,
    Namespace,
    Node,
    NodeSpec,
    PersistentVolume,
    PersistentVolumeClaim,
    PersistentVolumeClaimSpec,
    PersistentVolumeClaimVolumeSource,
    PersistentVolumeSpec,
    Pod,
    PodSecurityContext,
    PodTemplate,
    Probe,
    ReplicationController,
    ReplicationControllerSpec,
    ResourceQuota,
    ResourceQuotaSpec,
    ResourceRequirements,
    Secret,
    Service,
    ServiceAccount,
    ServicePort,
    ServiceSpec,
    TCPSocketAction,
    Volume,
)
from avionix.kube.reference import ObjectReference
from avionix.testing import kubectl_get
from avionix.testing.installation_context import ChartInstallationContext
from avionix.tests.utils import get_event_info, get_pod_with_options


def test_config_map(chart_info: ChartInfo, config_map: ConfigMap):
    builder = ChartBuilder(chart_info, [config_map])
    with ChartInstallationContext(builder):
        config_maps = kubectl_get("configmaps")
        assert config_maps["NAME"][0] == "test-config-map"
        assert config_maps["DATA"][0] == "1"


@pytest.fixture
def endpoints_metadata():
    return ObjectMeta(name="test-endpoints")


@pytest.fixture
def endpoints_no_subset(endpoints_metadata):
    return Endpoints(endpoints_metadata)


@pytest.fixture()
def endpoints_with_subset(endpoints_metadata):
    return Endpoints(
        endpoints_metadata,
        subsets=[
            EndpointSubset(
                addresses=[EndpointAddress("local", "10.9.8.7", None)],
                not_ready_addresses=None,
                ports=None,
            )
        ],
    )


def get_endpoints_info():
    info = DataFrame(kubectl_get("endpoints"))
    return info[info["NAME"] != "kubernetes"].reset_index(drop=True)


def test_endpoints_no_subset(chart_info: ChartInfo, endpoints_no_subset: Endpoints):
    builder = ChartBuilder(chart_info, [endpoints_no_subset])
    with ChartInstallationContext(builder):
        endpoints_info = get_endpoints_info()
        assert endpoints_info["NAME"][0] == "test-endpoints"
        assert endpoints_info["ENDPOINTS"][0] == "<none>"


def test_endpoints_with_subset(chart_info: ChartInfo, endpoints_with_subset: Endpoints):
    builder = ChartBuilder(chart_info, [endpoints_with_subset])
    with ChartInstallationContext(builder):
        endpoints_info = get_endpoints_info()
        assert endpoints_info["NAME"][0] == "test-endpoints"
        assert endpoints_info["ENDPOINTS"][0] == "10.9.8.7"


@pytest.fixture
def empty_event(object_meta_event, event_obj_ref):
    return Event(object_meta_event, event_obj_ref)


@pytest.fixture
def non_empty_event(object_meta_event, event_obj_ref):
    return Event(
        object_meta_event,
        event_obj_ref,
        message="test message",
        reason="testing",
        type="test-type",
    )


def test_create_empty_event(chart_info: ChartInfo, empty_event: Event):
    builder = ChartBuilder(chart_info, [empty_event])
    with ChartInstallationContext(builder):
        event_info = get_event_info()
        assert event_info["TYPE"][0] == ""
        assert event_info["REASON"][0] == ""
        assert event_info["OBJECT"][0] == "objectreference/test-ref"
        assert event_info["MESSAGE"][0] == ""


def test_create_nonempty_event(chart_info: ChartInfo, non_empty_event: Event):
    builder = ChartBuilder(chart_info, [non_empty_event])
    with ChartInstallationContext(builder):
        event_info = get_event_info()
        assert event_info["TYPE"][0] == "test-type"
        assert event_info["REASON"][0] == "testing"
        assert event_info["OBJECT"][0] == "objectreference/test-ref"
        assert event_info["MESSAGE"][0] == "test message"


@pytest.fixture
def limit_range():
    return LimitRange(
        ObjectMeta(name="test-range"),
        LimitRangeSpec(limits=[LimitRangeItem({}, {}, {}, {})]),
    )


def test_create_limitrange(chart_info, limit_range):
    builder = ChartBuilder(chart_info, [limit_range])
    with ChartInstallationContext(builder):
        namespace_info = kubectl_get("limitranges")
        assert namespace_info["NAME"][0] == "test-range"


@pytest.fixture
def namespace():
    return Namespace(ObjectMeta(name="test-namespace"))


def test_create_namespace(chart_info, namespace):
    builder = ChartBuilder(chart_info, [namespace])
    with ChartInstallationContext(builder):
        namespace_info = kubectl_get("namespaces")
        assert "test-namespace" in namespace_info["NAME"]


@pytest.fixture
def node_metadata():
    return ObjectMeta(name="test-node")


@pytest.fixture
def node(node_metadata):
    return Node(node_metadata, NodeSpec(external_id="12345", pod_cidr="10.0.0.0/24"))


def get_node_info():
    node_info = DataFrame(kubectl_get("nodes"))
    return node_info[node_info["NAME"] != "minikube"].reset_index(drop=True)


def test_create_non_empty_node(chart_info, node):
    builder = ChartBuilder(chart_info, [node])
    with ChartInstallationContext(builder):
        node_info = get_node_info()
        assert node_info["NAME"][0] == "test-node"
        assert node_info["STATUS"][0] == "Unknown"
        assert node_info["VERSION"][0] == ""


@pytest.fixture
def access_modes():
    return ["ReadWriteMany"]


modes_expected_value = "RWX"


@pytest.fixture
def persistent_volume(access_modes):
    return PersistentVolume(
        ObjectMeta(name="test-persistent-volume"),
        PersistentVolumeSpec(
            access_modes,
            capacity={"storage": 1},
            host_path=HostPathVolumeSource("/home/test/tmp"),
            storage_class_name="standard",
        ),
    )


def test_persistent_volume(chart_info, persistent_volume):
    builder = ChartBuilder(chart_info, [persistent_volume])
    with ChartInstallationContext(builder):
        volume_info = kubectl_get("persistentvolumes")
        assert volume_info["NAME"][0] == "test-persistent-volume"
        assert volume_info["CAPACITY"][0] == "1"
        assert volume_info["ACCESS MODES"][0] == modes_expected_value


@pytest.fixture
def empty_persistent_volume_claim(access_modes):
    return PersistentVolumeClaim(
        ObjectMeta(name="test-persistent-volume-claim"),
        PersistentVolumeClaimSpec(
            access_modes, ResourceRequirements(requests={"storage": 1}),
        ),
    )


def test_empty_persistent_volume_claim(chart_info, empty_persistent_volume_claim):
    builder = ChartBuilder(chart_info, [empty_persistent_volume_claim])
    with ChartInstallationContext(builder):
        volume_info = kubectl_get("persistentvolumeclaims")
        assert volume_info["NAME"][0] == "test-persistent-volume-claim"
        assert volume_info["CAPACITY"][0] == "1"
        assert volume_info["ACCESS MODES"][0] == modes_expected_value


def test_create_pod(chart_info: ChartInfo, pod: Pod):
    builder = ChartBuilder(chart_info, [pod])
    with ChartInstallationContext(builder):
        pods_info = kubectl_get("pods")
        assert pods_info["NAME"][0] == "test-pod"
        assert pods_info["READY"][0] == "1/1"
        assert pods_info["STATUS"][0] == "Running"


@pytest.fixture
def pod_template(pod_template_spec):
    return PodTemplate(ObjectMeta(name="test-pod-template"), pod_template_spec)


def test_create_pod_template(chart_info: ChartInfo, pod_template: PodTemplate):
    builder = ChartBuilder(chart_info, [pod_template])
    with ChartInstallationContext(builder):
        template_info = kubectl_get("podtemplates")
        assert template_info["NAME"][0] == "test-pod-template"
        assert template_info["CONTAINERS"][0] == "test-container-0"
        assert template_info["IMAGES"][0] == "k8s.gcr.io/echoserver:1.4"


@pytest.fixture
def replication_controller(pod_template_spec):
    return ReplicationController(
        ObjectMeta(name="test-replication-controller"),
        spec=ReplicationControllerSpec(pod_template_spec, selector={"type": "master"}),
    )


def test_replication_controller(chart_info, replication_controller):
    builder = ChartBuilder(chart_info, [replication_controller])
    with ChartInstallationContext(builder):
        replication_info = kubectl_get("replicationcontrollers")
        assert replication_info["NAME"][0] == "test-replication-controller"
        assert replication_info["DESIRED"][0] == "1"
        assert replication_info["CURRENT"][0] == "1"


@pytest.fixture
def resource_quota():
    return ResourceQuota(
        ObjectMeta(name="test-resource-quota"), spec=ResourceQuotaSpec(hard={"cpu": 1})
    )


def test_resource_quota(chart_info, resource_quota):
    builder = ChartBuilder(chart_info, [resource_quota])
    with ChartInstallationContext(builder):
        quota_info = kubectl_get("resourcequotas")
        assert quota_info["NAME"][0] == "test-resource-quota"
        assert quota_info["REQUEST"][0] == "cpu: 0/1"


@pytest.fixture
def empty_secret():
    return Secret(ObjectMeta(name="test-secret"))


@pytest.fixture
def non_empty_secret():
    return Secret(ObjectMeta(name="test-secret"), {"secret_key": "test"})


def get_secret_info():
    info = DataFrame(kubectl_get("secrets"))
    return info[info["NAME"] == "test-secret"].reset_index(drop=True)


def test_empty_secret(chart_info, empty_secret):
    builder = ChartBuilder(chart_info, [empty_secret])
    with ChartInstallationContext(builder):
        secret_info = get_secret_info()
        assert secret_info["NAME"][0] == "test-secret"
        assert secret_info["DATA"][0] == "0"


def test_non_empty_secret(chart_info, non_empty_secret):
    builder = ChartBuilder(chart_info, [non_empty_secret])
    with ChartInstallationContext(builder):
        secret_info = get_secret_info()
        assert secret_info["NAME"][0] == "test-secret"
        assert secret_info["DATA"][0] == "1"


@pytest.fixture
def empty_service():
    return Service(ObjectMeta(name="test-service"), ServiceSpec([ServicePort(80)]))


@pytest.fixture
def nonempty_service():
    return Service(
        ObjectMeta(name="test-service"),
        ServiceSpec(
            [
                ServicePort(80, name="port1"),
                ServicePort(8080, protocol="UDP", name="port2"),
            ],
            external_ips=["152.0.0.0"],
        ),
    )


def get_service_info():
    info = DataFrame(kubectl_get("services"))
    return info[info["NAME"] != "kubernetes"].reset_index(drop=True)


def test_empty_service(chart_info, empty_service):
    builder = ChartBuilder(chart_info, [empty_service])
    with ChartInstallationContext(builder):
        service_info = get_service_info()
        assert service_info["NAME"][0] == "test-service"
        assert service_info["PORT(S)"][0] == "80/TCP"


def test_nonempty_service(chart_info, nonempty_service):
    builder = ChartBuilder(chart_info, [nonempty_service])
    with ChartInstallationContext(builder):
        service_info = get_service_info()
        assert service_info["NAME"][0] == "test-service"
        assert service_info["PORT(S)"][0] == "80/TCP,8080/UDP"
        assert service_info["EXTERNAL-IP"][0] == "152.0.0.0"


@pytest.fixture
def nonempty_service_account():
    return ServiceAccount(
        ObjectMeta(name="test-service-account"),
        secrets=[ObjectReference("test", name="test-ref")],
    )


def get_service_account_info():
    info = DataFrame(kubectl_get("serviceaccounts"))
    return info[info["NAME"] != "default"].reset_index(drop=True)


def test_empty_service_account(chart_info, empty_service_account):
    builder = ChartBuilder(chart_info, [empty_service_account])
    with ChartInstallationContext(builder):
        service_account_info = get_service_account_info()
        assert service_account_info["NAME"][0] == "test-service-account"


def test_nonempty_service_account(chart_info, nonempty_service_account):
    builder = ChartBuilder(chart_info, [nonempty_service_account])
    with ChartInstallationContext(builder):
        service_account_info = get_service_account_info()
        assert service_account_info["NAME"][0] == "test-service-account"
        assert service_account_info["SECRETS"][0] == "2"


@pytest.fixture
def binding():
    binding = Binding(
        metadata=ObjectMeta(name="test-pod"),
        target=ObjectReference("test", name="test_object", namespace="test"),
    )
    return binding


@pytest.mark.skip(reason="Still need to figure out this test")
def test_create_binding(chart_info: ChartInfo, binding: Binding, pod: Pod):
    builder = ChartBuilder(chart_info, [binding, pod])
    with ChartInstallationContext(builder):
        kubectl_get("bindings")


@pytest.fixture
def persistent_volume_claim(persistent_volume):
    return PersistentVolumeClaim(
        ObjectMeta(name="test-pv-claim"),
        PersistentVolumeClaimSpec(
            persistent_volume.spec.accessModes,
            resources=ResourceRequirements(
                requests={"storage": persistent_volume.spec.capacity["storage"]}
            ),
        ),
    )


@pytest.fixture
def pod_w_persistent_volume(persistent_volume_claim):
    volume = Volume(
        "test-volume",
        persistent_volume_claim=PersistentVolumeClaimVolumeSource(
            persistent_volume_claim.metadata.name, read_only=True
        ),
    )
    return get_pod_with_options(volume)


def test_pod_w_persistent_volume(
    chart_info, pod_w_persistent_volume, persistent_volume, persistent_volume_claim
):
    builder = ChartBuilder(
        chart_info,
        [persistent_volume, pod_w_persistent_volume, persistent_volume_claim],
    )
    with ChartInstallationContext(builder):
        # Check pod ready
        pod_info = kubectl_get("pods", wide=True)
        assert pod_info["NAME"][0] == "test-pod"
        assert pod_info["READY"][0] == "1/1"

        # Check volume bound
        volume_info = kubectl_get("persistentvolume")
        assert volume_info["NAME"][0] == "test-persistent-volume"
        assert volume_info["CAPACITY"][0] == "1"
        assert volume_info["ACCESS MODES"][0] == "RWX"
        assert volume_info["RECLAIM POLICY"][0] == "Retain"
        assert volume_info["STATUS"][0] == "Bound"
        assert volume_info["CLAIM"][0] == "default/test-pv-claim"

        claim_info = kubectl_get("persistentvolumeclaims")
        assert claim_info["NAME"][0] == "test-pv-claim"
        assert claim_info["STATUS"][0] == "Bound"
        assert claim_info["CAPACITY"][0] == "1"
        assert claim_info["ACCESS MODES"][0] == "RWX"


@pytest.fixture
def pod_w_security_context():
    security_context = PodSecurityContext(1000)
    return get_pod_with_options(security_context=security_context)


def test_pod_security_context(pod_w_security_context, chart_info):
    builder = ChartBuilder(chart_info, [pod_w_security_context])
    with ChartInstallationContext(builder):
        pod_info = kubectl_get("pods")
        assert pod_info["NAME"][0] == "test-pod"
        assert pod_info["READY"][0] == "1/1"
        assert pod_info["STATUS"][0] == "Running"


@pytest.mark.parametrize(
    "probe",
    [
        Probe(
            http_get=HTTPGetAction("/", 8080), period_seconds=1, failure_threshold=10
        ),
        Probe(
            exec=ExecAction(["echo", "good"]), period_seconds=1, failure_threshold=10
        ),
        Probe(tcp_socket=TCPSocketAction(8080), period_seconds=1, failure_threshold=10),
    ],
)
def test_container_probes(chart_info, probe: Probe):
    pod = get_pod_with_options(readiness_probe=probe)
    builder = ChartBuilder(chart_info, [pod])
    with ChartInstallationContext(
        builder, expected_status={"1/1"}, status_field="READY"
    ):
        pod_info = kubectl_get("pods")
        assert pod_info["NAME"][0] == "test-pod"
        assert pod_info["READY"][0] == "1/1"
        assert pod_info["STATUS"][0] == "Running"
