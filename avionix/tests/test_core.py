from typing import List

from pandas import DataFrame
import pytest

from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kube.base_objects import KubernetesBaseObject
from avionix.kube.core import (
    Affinity,
    Binding,
    Capabilities,
    ClientIPConfig,
    ConfigMap,
    ConfigMapEnvSource,
    ConfigMapKeySelector,
    ConfigMapProjection,
    DownwardAPIProjection,
    DownwardAPIVolumeFile,
    EndpointAddress,
    Endpoints,
    EndpointSubset,
    EnvFromSource,
    EnvVar,
    EnvVarSource,
    Event,
    ExecAction,
    Handler,
    HostAlias,
    HostPathVolumeSource,
    HTTPGetAction,
    HTTPHeader,
    KeyToPath,
    LabelSelector,
    Lifecycle,
    LimitRange,
    LimitRangeItem,
    LimitRangeSpec,
    Namespace,
    Node,
    NodeAffinity,
    NodeSelector,
    NodeSelectorRequirement,
    NodeSelectorTerm,
    NodeSpec,
    ObjectFieldSelector,
    PersistentVolume,
    PersistentVolumeClaim,
    PersistentVolumeClaimSpec,
    PersistentVolumeClaimVolumeSource,
    PersistentVolumeSpec,
    Pod,
    PodAffinity,
    PodAffinityTerm,
    PodAntiAffinity,
    PodDNSConfig,
    PodDNSConfigOption,
    PodSecurityContext,
    PodTemplate,
    PreferredSchedulingTerm,
    Probe,
    ProjectedVolumeSource,
    ReplicationController,
    ReplicationControllerSpec,
    ResourceFieldSelector,
    ResourceQuota,
    ResourceQuotaSpec,
    ResourceRequirements,
    ScopedResourceSelectorRequirement,
    ScopeSelector,
    Secret,
    SecretEnvSource,
    SecretKeySelector,
    SecretProjection,
    SecurityContext,
    SELinuxOptions,
    Service,
    ServiceAccount,
    ServicePort,
    ServiceSpec,
    SessionAffinityConfig,
    Sysctl,
    TCPSocketAction,
    TopologySpreadConstraint,
    Volume,
    VolumeMount,
    VolumeProjection,
    WeightedPodAffinityTerm,
    WindowsSecurityContextOptions,
)
from avionix.kube.meta import LabelSelectorRequirement
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


@pytest.mark.parametrize(
    "resource_quota",
    [
        ResourceQuota(
            ObjectMeta(name="test-resource-quota"),
            spec=ResourceQuotaSpec(hard={"cpu": 1}),
        ),
        ResourceQuota(
            ObjectMeta(name="test-resource-quota-w-scope"),
            spec=ResourceQuotaSpec(
                hard={"cpu": 1},
                scope_selector=ScopeSelector(
                    [ScopedResourceSelectorRequirement("DoesNotExist", "PriorityClass")]
                ),
            ),
        ),
    ],
)
def test_resource_quota(chart_info, resource_quota):
    builder = ChartBuilder(chart_info, [resource_quota])
    with ChartInstallationContext(builder):
        quota_info = kubectl_get("resourcequotas")
        assert quota_info["NAME"][0] == resource_quota.metadata.name
        assert quota_info["REQUEST"][0] == "cpu: 0/1"


def get_secret_info():
    info = DataFrame(kubectl_get("secrets"))
    return info[info["NAME"] == "test-secret"].reset_index(drop=True)


@pytest.mark.parametrize("secret_data", [{"secret_key": "test"}, None, {}])
def test_secret(chart_info, secret_data: dict):
    builder = ChartBuilder(
        chart_info, [Secret(ObjectMeta(name="test-secret"), secret_data)]
    )
    with ChartInstallationContext(builder):
        secret_info = get_secret_info()
        assert secret_info["NAME"][0] == "test-secret"
        assert secret_info["DATA"][0] == str(len(secret_data)) if secret_data else "0"


def get_service_info():
    info = DataFrame(kubectl_get("services"))
    return info[info["NAME"] != "kubernetes"].reset_index(drop=True)


@pytest.mark.parametrize(
    "service_spec",
    [
        ServiceSpec([ServicePort(80)]),
        ServiceSpec(
            [
                ServicePort(80, name="port1"),
                ServicePort(8080, protocol="UDP", name="port2"),
            ],
            external_ips=["152.0.0.0"],
        ),
        ServiceSpec(
            [ServicePort(80)],
            session_affinity_config=SessionAffinityConfig(ClientIPConfig(10)),
        ),
    ],
)
def test_service(chart_info, service_spec: ServiceSpec):
    builder = ChartBuilder(
        chart_info, [Service(ObjectMeta(name="test-service"), service_spec)]
    )
    with ChartInstallationContext(builder):
        service_info = get_service_info()
        assert service_info["NAME"][0] == "test-service"
        assert service_info["PORT(S)"][0] == ",".join(
            [
                f"{port.port}/{port.protocol if port.protocol else 'TCP'}"
                for port in service_spec.ports
            ]
        )
        assert service_info["EXTERNAL-IP"][0] == (
            service_spec.externalIPs[0] if service_spec.externalIPs else "<none>"
        )


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
            # volume_mode="Block"
        ),
    )


@pytest.mark.parametrize(
    "mounts_or_devices",
    [
        {"volume_mount": VolumeMount("test-volume", "~/tmp")},
        # {"volume_device": VolumeDevice("test-volume", "~/tmp")},
    ],
)
def test_persistent_volume_on_pod(
    chart_info, persistent_volume, persistent_volume_claim, mounts_or_devices: dict
):
    builder = ChartBuilder(
        chart_info,
        [
            persistent_volume,
            get_pod_with_options(
                Volume(
                    "test-volume",
                    persistent_volume_claim=PersistentVolumeClaimVolumeSource(
                        persistent_volume_claim.metadata.name, read_only=True
                    ),
                ),
                # command=["bash", "-c", "mkdir ~/tmp; nginx -g 'daemon off;'"],
                **mounts_or_devices,
            ),
            persistent_volume_claim,
        ],
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


@pytest.mark.parametrize(
    "volume",
    [
        Volume(
            name="config-map-projection",
            projected=ProjectedVolumeSource(
                [
                    VolumeProjection(
                        ConfigMapProjection(
                            "test", True, items=[KeyToPath("test", "tmp/")]
                        ),
                    )
                ],
            ),
        ),
        Volume(
            name="project-downward-api",
            projected=ProjectedVolumeSource(
                [
                    VolumeProjection(
                        downward_api=DownwardAPIProjection(
                            [
                                DownwardAPIVolumeFile(
                                    "labels", ObjectFieldSelector("metadata.labels")
                                )
                            ]
                        )
                    )
                ]
            ),
        ),
        Volume(
            name="project-secret",
            projected=ProjectedVolumeSource(
                [VolumeProjection(secret=SecretProjection("my-secret", True))]
            ),
        ),
        # Volume(
        #     name="project-service-account-token",
        #     projected=ProjectedVolumeSource(
        #         [VolumeProjection(
        #             service_account_token=ServiceAccountTokenProjection("vault-token"))]
        #     )
        # )
    ],
)
def test_projected_volumes(chart_info, volume: Volume):
    builder = ChartBuilder(chart_info, [get_pod_with_options(volume)])
    with ChartInstallationContext(builder):
        pod_info = kubectl_get("pods", wide=True)
        assert pod_info["NAME"][0] == "test-pod"
        assert pod_info["READY"][0] == "1/1"


@pytest.mark.parametrize(
    "pod,other_resources",
    [
        (get_pod_with_options(), None),
        (
            get_pod_with_options(
                name="pod-security-1", pod_security_context=PodSecurityContext(10000)
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="pod-security-2",
                pod_security_context=PodSecurityContext(
                    sysctls=[Sysctl("kernel.shm_rmid_forced", "0")]
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="env-var-config-map",
                environment_var=EnvVar(
                    "from_config_map",
                    value_from=EnvVarSource(ConfigMapKeySelector("config-map", "key")),
                ),
            ),
            [ConfigMap(ObjectMeta(name="config-map"), {"key": "value"})],
        ),
        (
            get_pod_with_options(
                name="env-var-objectfield",
                environment_var=EnvVar(
                    "from_field_selector",
                    value_from=EnvVarSource(
                        field_ref=ObjectFieldSelector("metadata.name")
                    ),
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="env-var-resource",
                environment_var=EnvVar(
                    "from_resource_field_selector",
                    value_from=EnvVarSource(
                        resource_field_ref=ResourceFieldSelector(
                            "test-container-0", "requests.memory"
                        )
                    ),
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="env-var-secret-key",
                environment_var=EnvVar(
                    "from_resource_field_selector",
                    value_from=EnvVarSource(
                        secret_key_ref=SecretKeySelector("test-secret", "secret_key")
                    ),
                ),
            ),
            [Secret(ObjectMeta(name="test-secret"), {"secret_key": "test"})],
        ),
        (
            get_pod_with_options(
                name="secuirty-context-all",
                container_security_context=SecurityContext(
                    capabilities=Capabilities(["ALL"])
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="security-context-drop",
                container_security_context=SecurityContext(
                    capabilities=Capabilities(drop=["NET_BIND_SERVICE"])
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="security-context-linux",
                container_security_context=SecurityContext(
                    se_linux_options=SELinuxOptions(level="2")
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="lifecyle-pre-stop",
                lifecycle=Lifecycle(pre_stop=Handler(tcp_socket=TCPSocketAction(8080))),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="lifecyle-post-start",
                lifecycle=Lifecycle(post_start=Handler(ExecAction(["echo", "yes"]))),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="lifecyle-http",
                lifecycle=Lifecycle(
                    post_start=Handler(http_get=HTTPGetAction("/my/path", 8080))
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="host-alias", host_alias=HostAlias(["test.com"], "129.0.0.0")
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="security-context-windows",
                container_security_context=SecurityContext(
                    windows_options=WindowsSecurityContextOptions("test", "test")
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="env-from",
                env_from=[
                    EnvFromSource(ConfigMapEnvSource("config-map")),
                    EnvFromSource(secret_ref=SecretEnvSource("test-secret")),
                ],
            ),
            [
                ConfigMap(ObjectMeta(name="config-map"), {"key": "value"}),
                Secret(ObjectMeta(name="test-secret"), {"secret_key": "test"}),
            ],
        ),
        (
            get_pod_with_options(
                name="topology-spread",
                topology_spread=TopologySpreadConstraint(1, "t", "ScheduleAnyway"),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="dns-config-option",
                dns_config=PodDNSConfig(options=[PodDNSConfigOption("test")]),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="dns-config-no-option", dns_config=PodDNSConfig(["1.1.1.1"])
            ),
            None,
        ),
        (get_pod_with_options(name="epehemeral", ephemeral=True), None),
        (
            get_pod_with_options(
                name="required-node-affinity",
                affinity=Affinity(
                    node_affinity=NodeAffinity(
                        required_during_scheduling_ignored_during_execution=NodeSelector(
                            [
                                NodeSelectorTerm(
                                    match_expressions=[
                                        NodeSelectorRequirement(
                                            "kubernetes.io/os", "Exists"
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="node-affinity",
                affinity=Affinity(
                    node_affinity=NodeAffinity(
                        [
                            PreferredSchedulingTerm(
                                NodeSelectorTerm(
                                    match_fields=[
                                        NodeSelectorRequirement(
                                            "metadata.name", "In", ["minikube"]
                                        ),
                                    ]
                                ),
                                weight=2,
                            ),
                            PreferredSchedulingTerm(
                                NodeSelectorTerm(
                                    match_expressions=[
                                        NodeSelectorRequirement("test", "Exists")
                                    ],
                                ),
                                weight=1,
                            ),
                        ],
                    )
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="pod-affinity",
                affinity=Affinity(
                    PodAffinity(
                        [
                            WeightedPodAffinityTerm(
                                PodAffinityTerm(
                                    "minikube.k8s.io/name", namespaces=["default"],
                                ),
                                weight=10,
                            ),
                            WeightedPodAffinityTerm(
                                PodAffinityTerm(topology_key="minikube.k8s.io/name"),
                                weight=3,
                            ),
                        ],
                    ),
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="required-pod-affinity",
                affinity=Affinity(
                    PodAffinity(
                        required_during_scheduling_ignored_during_execution=[
                            PodAffinityTerm(
                                "kubernetes.io/arch",
                                LabelSelector(
                                    match_expressions=[
                                        LabelSelectorRequirement(
                                            "app.kubernetes.io/managed-by", "Exists",
                                        )
                                    ],
                                ),
                            ),
                        ]
                    ),
                ),
            ),
            [get_pod_with_options(name="affinity-pod")],
        ),
        (
            get_pod_with_options(
                name="anti-affinity",
                affinity=Affinity(
                    pod_anti_affinity=PodAntiAffinity(
                        [
                            WeightedPodAffinityTerm(
                                PodAffinityTerm("T", namespaces=["default"]), weight=2
                            )
                        ],
                    ),
                ),
            ),
            None,
        ),
        (
            get_pod_with_options(
                name="required-anti-affinity",
                affinity=Affinity(
                    pod_anti_affinity=PodAntiAffinity(
                        required_during_scheduling_ignored_during_execution=[
                            PodAffinityTerm(topology_key="t")
                        ],
                    ),
                ),
            ),
            None,
        ),
    ],
)
def test_pod(chart_info, pod: Pod, other_resources: List[KubernetesBaseObject]):
    if other_resources is None:
        other_resources = []
    builder = ChartBuilder(chart_info, [pod] + other_resources)
    with ChartInstallationContext(builder):
        pod_info = DataFrame(kubectl_get("pods"))
        pod_info = pod_info[pod_info["NAME"] == pod.metadata.name].reset_index(
            drop=True
        )
        assert pod_info["NAME"][0] == pod.metadata.name
        assert pod_info["READY"][0] == "1/1"
        assert pod_info["STATUS"][0] == "Running"


@pytest.mark.parametrize(
    "probe",
    [
        Probe(
            http_get=HTTPGetAction("/", 8080, [HTTPHeader("GET", "yes")]),
            period_seconds=1,
            failure_threshold=10,
        ),
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
