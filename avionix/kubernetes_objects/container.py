from datetime import time
from typing import List, Optional

from avionix.kubernetes_objects.action import Lifecycle, Probe
from avionix.kubernetes_objects.env import EnvFromSource, EnvVar
from avionix.kubernetes_objects.general import ResourceRequirements
from avionix.kubernetes_objects.security import SecurityContext
from avionix.kubernetes_objects.volume import VolumeDevice, VolumeMount
from avionix.yaml.yaml_handling import HelmYaml


class ContainerPort(HelmYaml):
    """
    :param container_port:Number of port to expose on the pod's IP address. This must \
        be a valid port number, 0 < x < 65536.
    :type container_port: int
    :param host_ip:What host IP to bind the external port to.
    :type host_ip: str
    :param host_port:Number of port to expose on the host. If specified, this must be \
        a valid port number, 0 < x < 65536. If HostNetwork is specified, this must \
        match ContainerPort. Most containers do not need this.
    :type host_port: Optional[int]
    :param name:If specified, this must be an IANA_SVC_NAME and unique within the pod. \
        Each named port in a pod must have a unique name. Name for the port that can \
        be referred to by services.
    :type name: Optional[str]
    :param protocol:Protocol for port. Must be UDP, TCP, or SCTP. Defaults to "TCP".
    :type protocol: Optional[str]
    """

    def __init__(
        self,
        container_port: int,
        host_ip: str,
        host_port: Optional[int] = None,
        name: Optional[str] = None,
        protocol: Optional[str] = None,
    ):
        self.containerPort = container_port
        self.hostIP = host_ip
        self.hostPort = host_port
        self.name = name
        self.protocol = protocol


class EphemeralContainer(HelmYaml):
    """
    :param image:Docker image name. More info: \
        https://kubernetes.io/docs/concepts/containers/images
    :type image: str
    :param startup_probe:Probes are not allowed for ephemeral containers.
    :type startup_probe: Probe
    :param target_container_name:If set, the name of the container from PodSpec that \
        this ephemeral container targets. The ephemeral container will be run in the \
        namespaces (IPC, PID, etc) of this container. If not set then the ephemeral \
        container is run in whatever namespaces are shared for the pod. Note that the \
        container runtime must support this feature.
    :type target_container_name: str
    :param args:Arguments to the entrypoint. The docker image's CMD is used if this is \
        not provided. Variable references $(VAR_NAME) are expanded using the \
        container's environment. If a variable cannot be resolved, the reference in \
        the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with \
        a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, \
        regardless of whether the variable exists or not. Cannot be updated. More \
        info: \
        https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell  # noqa
    :type args: Optional[List[str]]
    :param command:Entrypoint array. Not executed within a shell. The docker image's \
        ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) \
        are expanded using the container's environment. If a variable cannot be \
        resolved, the reference in the input string will be unchanged. The $(VAR_NAME) \
        syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references \
        will never be expanded, regardless of whether the variable exists or not. \
        Cannot be updated. More info: \
        https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell  # noqa
    :type command: Optional[List[str]]
    :param env:List of environment variables to set in the container. Cannot be \
        updated.
    :type env: Optional[List[EnvVar]]
    :param env_from:List of sources to populate environment variables in the \
        container. The keys defined within a source must be a C_IDENTIFIER. All \
        invalid keys will be reported as an event when the container is starting. When \
        a key exists in multiple sources, the value associated with the last source \
        will take precedence. Values defined by an Env with a duplicate key will take \
        precedence. Cannot be updated.
    :type env_from: Optional[List[EnvFromSource]]
    :param image_pull_policy:Image pull policy. One of Always, Never, IfNotPresent. \
        Defaults to Always if :latest tag is specified, or IfNotPresent otherwise. \
        Cannot be updated. More info: \
        https://kubernetes.io/docs/concepts/containers/images#updating-images
    :type image_pull_policy: Optional[str]
    :param lifecycle:Lifecycle is not allowed for ephemeral containers.
    :type lifecycle: Optional[Lifecycle]
    :param liveness_probe:Probes are not allowed for ephemeral containers.
    :type liveness_probe: Optional[Probe]
    :param name:Name of the ephemeral container specified as a DNS_LABEL. This name \
        must be unique among all containers, init containers and ephemeral containers.
    :type name: Optional[str]
    :param ports:Ports are not allowed for ephemeral containers.
    :type ports: Optional[List[ContainerPort]]
    :param readiness_probe:Probes are not allowed for ephemeral containers.
    :type readiness_probe: Optional[Probe]
    :param resources:Resources are not allowed for ephemeral containers. Ephemeral \
        containers use spare resources already allocated to the pod.
    :type resources: Optional[ResourceRequirements]
    :param security_context:SecurityContext is not allowed for ephemeral containers.
    :type security_context: Optional[SecurityContext]
    :param stdin:Whether this container should allocate a buffer for stdin in the \
        container runtime. If this is not set, reads from stdin in the container will \
        always result in EOF. Default is false.
    :type stdin: Optional[bool]
    :param stdin_once:Whether the container runtime should close the stdin channel \
        after it has been opened by a single attach. When stdin is true the stdin \
        stream will remain open across multiple attach sessions. If stdinOnce is set \
        to true, stdin is opened on container start, is empty until the first client \
        attaches to stdin, and then remains open and accepts data until the client \
        disconnects, at which time stdin is closed and remains closed until the \
        container is restarted. If this flag is false, a container processes that \
        reads from stdin will never receive an EOF. Default is false
    :type stdin_once: Optional[bool]
    :param termination_message_path:Optional: Path at which the file to which the \
        container's termination message will be written is mounted into the \
        container's filesystem. Message written is intended to be brief final status, \
        such as an assertion failure message. Will be truncated by the node if greater \
        than 4096 bytes. The total message length across all containers will be \
        limited to 12kb. Defaults to /dev/termination-log. Cannot be updated.
    :type termination_message_path: Optional[str]
    :param termination_message_policy:Indicate how the termination message should be \
        populated. File will use the contents of terminationMessagePath to populate \
        the container status message on both success and failure. \
        FallbackToLogsOnError will use the last chunk of container log output if the \
        termination message file is empty and the container exited with an error. The \
        log output is limited to 2048 bytes or 80 lines, whichever is smaller. \
        Defaults to File. Cannot be updated.
    :type termination_message_policy: Optional[str]
    :param tty:Whether this container should allocate a TTY for itself, also requires \
        'stdin' to be true. Default is false.
    :type tty: Optional[bool]
    :param volume_devices:volumeDevices is the list of block devices to be used by the \
        container.
    :type volume_devices: Optional[List[VolumeDevice]]
    :param volume_mounts:Pod volumes to mount into the container's filesystem. Cannot \
        be updated.
    :type volume_mounts: Optional[List[VolumeMount]]
    :param working_dir:Container's working directory. If not specified, the container \
        runtime's default will be used, which might be configured in the container \
        image. Cannot be updated.
    :type working_dir: Optional[str]
    """

    def __init__(
        self,
        image: str,
        startup_probe: Probe,
        target_container_name: str,
        args: Optional[List[str]] = None,
        command: Optional[List[str]] = None,
        env: Optional[List[EnvVar]] = None,
        env_from: Optional[List[EnvFromSource]] = None,
        image_pull_policy: Optional[str] = None,
        lifecycle: Optional[Lifecycle] = None,
        liveness_probe: Optional[Probe] = None,
        name: Optional[str] = None,
        ports: Optional[List[ContainerPort]] = None,
        readiness_probe: Optional[Probe] = None,
        resources: Optional[ResourceRequirements] = None,
        security_context: Optional[SecurityContext] = None,
        stdin: Optional[bool] = None,
        stdin_once: Optional[bool] = None,
        termination_message_path: Optional[str] = None,
        termination_message_policy: Optional[str] = None,
        tty: Optional[bool] = None,
        volume_devices: Optional[List[VolumeDevice]] = None,
        volume_mounts: Optional[List[VolumeMount]] = None,
        working_dir: Optional[str] = None,
    ):
        self.image = image
        self.startupProbe = startup_probe
        self.targetContainerName = target_container_name
        self.args = args
        self.command = command
        self.env = env
        self.envFrom = env_from
        self.imagePullPolicy = image_pull_policy
        self.lifecycle = lifecycle
        self.livenessProbe = liveness_probe
        self.name = name
        self.ports = ports
        self.readinessProbe = readiness_probe
        self.resources = resources
        self.securityContext = security_context
        self.stdin = stdin
        self.stdinOnce = stdin_once
        self.terminationMessagePath = termination_message_path
        self.terminationMessagePolicy = termination_message_policy
        self.tty = tty
        self.volumeDevices = volume_devices
        self.volumeMounts = volume_mounts
        self.workingDir = working_dir


class Container(HelmYaml):
    """
    :param args:Arguments to the entrypoint. The docker image's CMD is used if this is \
        not provided. Variable references $(VAR_NAME) are expanded using the \
        container's environment. If a variable cannot be resolved, the reference in \
        the input string will be unchanged. The $(VAR_NAME) syntax can be escaped with \
        a double $$, ie: $$(VAR_NAME). Escaped references will never be expanded, \
        regardless of whether the variable exists or not. Cannot be updated. More \
        info: \
        https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell  # noqa
    :type args: Optional[List[str]]
    :param command:Entrypoint array. Not executed within a shell. The docker image's \
        ENTRYPOINT is used if this is not provided. Variable references $(VAR_NAME) \
        are expanded using the container's environment. If a variable cannot be \
        resolved, the reference in the input string will be unchanged. The $(VAR_NAME) \
        syntax can be escaped with a double $$, ie: $$(VAR_NAME). Escaped references \
        will never be expanded, regardless of whether the variable exists or not. \
        Cannot be updated. More info: \
        https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/#running-a-command-in-a-shell  # noqa
    :type command: Optional[List[str]]
    :param env:List of environment variables to set in the container. Cannot be \
        updated.
    :type env: Optional[List[EnvVar]]
    :param env_from:List of sources to populate environment variables in the \
        container. The keys defined within a source must be a C_IDENTIFIER. All \
        invalid keys will be reported as an event when the container is starting. When \
        a key exists in multiple sources, the value associated with the last source \
        will take precedence. Values defined by an Env with a duplicate key will take \
        precedence. Cannot be updated.
    :type env_from: Optional[List[EnvFromSource]]
    :param image:Docker image name. More info: \
        https://kubernetes.io/docs/concepts/containers/images This field is optional \
        to allow higher level config management to default or override container \
        images in workload controllers like Deployments and StatefulSets.
    :type image: Optional[str]
    :param image_pull_policy:Image pull policy. One of Always, Never, IfNotPresent. \
        Defaults to Always if :latest tag is specified, or IfNotPresent otherwise. \
        Cannot be updated. More info: \
        https://kubernetes.io/docs/concepts/containers/images#updating-images
    :type image_pull_policy: Optional[str]
    :param lifecycle:Actions that the management system should take in response to \
        container lifecycle events. Cannot be updated.
    :type lifecycle: Optional[Lifecycle]
    :param liveness_probe:Periodic probe of container liveness. Container will be \
        restarted if the probe fails. Cannot be updated. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    :type liveness_probe: Optional[Probe]
    :param name:Name of the container specified as a DNS_LABEL. Each container in a \
        pod must have a unique name (DNS_LABEL). Cannot be updated.
    :type name: Optional[str]
    :param ports:List of ports to expose from the container. Exposing a port here \
        gives the system additional information about the network connections a \
        container uses, but is primarily informational. Not specifying a port here \
        DOES NOT prevent that port from being exposed. Any port which is listening on \
        the default "0.0.0.0" address inside a container will be accessible from the \
        network. Cannot be updated.
    :type ports: Optional[List[ContainerPort]]
    :param readiness_probe:Periodic probe of container service readiness. Container \
        will be removed from service endpoints if the probe fails. Cannot be updated. \
        More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    :type readiness_probe: Optional[Probe]
    :param resources:Compute Resources required by this container. Cannot be updated. \
        More info: \
        https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/  # noqa
    :type resources: Optional[ResourceRequirements]
    :param security_context:Security options the pod should run with. More info: \
        https://kubernetes.io/docs/concepts/policy/security-context/ More info: \
        https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
    :type security_context: Optional[SecurityContext]
    :param startup_probe:StartupProbe indicates that the Pod has successfully \
        initialized. If specified, no other probes are executed until this completes \
        successfully. If this probe fails, the Pod will be restarted, just as if the \
        livenessProbe failed. This can be used to provide different probe parameters \
        at the beginning of a Pod's lifecycle, when it might take a long time to load \
        data or warm a cache, than during steady-state operation. This cannot be \
        updated. This is a beta feature enabled by the StartupProbe feature flag. More \
        info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    :type startup_probe: Optional[Probe]
    :param stdin:Whether this container should allocate a buffer for stdin in the \
        container runtime. If this is not set, reads from stdin in the container will \
        always result in EOF. Default is false.
    :type stdin: Optional[bool]
    :param stdin_once:Whether the container runtime should close the stdin channel \
        after it has been opened by a single attach. When stdin is true the stdin \
        stream will remain open across multiple attach sessions. If stdinOnce is set \
        to true, stdin is opened on container start, is empty until the first client \
        attaches to stdin, and then remains open and accepts data until the client \
        disconnects, at which time stdin is closed and remains closed until the \
        container is restarted. If this flag is false, a container processes that \
        reads from stdin will never receive an EOF. Default is false
    :type stdin_once: Optional[bool]
    :param termination_message_path:Optional: Path at which the file to which the \
        container's termination message will be written is mounted into the \
        container's filesystem. Message written is intended to be brief final status, \
        such as an assertion failure message. Will be truncated by the node if greater \
        than 4096 bytes. The total message length across all containers will be \
        limited to 12kb. Defaults to /dev/termination-log. Cannot be updated.
    :type termination_message_path: Optional[str]
    :param termination_message_policy:Indicate how the termination message should be \
        populated. File will use the contents of terminationMessagePath to populate \
        the container status message on both success and failure. \
        FallbackToLogsOnError will use the last chunk of container log output if the \
        termination message file is empty and the container exited with an error. The \
        log output is limited to 2048 bytes or 80 lines, whichever is smaller. \
        Defaults to File. Cannot be updated.
    :type termination_message_policy: Optional[str]
    :param tty:Whether this container should allocate a TTY for itself, also requires \
        'stdin' to be true. Default is false.
    :type tty: Optional[bool]
    :param volume_devices:volumeDevices is the list of block devices to be used by the \
        container.
    :type volume_devices: Optional[List[VolumeDevice]]
    :param volume_mounts:Pod volumes to mount into the container's filesystem. Cannot \
        be updated.
    :type volume_mounts: Optional[List[VolumeMount]]
    :param working_dir:Container's working directory. If not specified, the container \
        runtime's default will be used, which might be configured in the container \
        image. Cannot be updated.
    :type working_dir: Optional[str]
    """

    def __init__(
        self,
        args: Optional[List[str]] = None,
        command: Optional[List[str]] = None,
        env: Optional[List[EnvVar]] = None,
        env_from: Optional[List[EnvFromSource]] = None,
        image: Optional[str] = None,
        image_pull_policy: Optional[str] = None,
        lifecycle: Optional[Lifecycle] = None,
        liveness_probe: Optional[Probe] = None,
        name: Optional[str] = None,
        ports: Optional[List[ContainerPort]] = None,
        readiness_probe: Optional[Probe] = None,
        resources: Optional[ResourceRequirements] = None,
        security_context: Optional[SecurityContext] = None,
        startup_probe: Optional[Probe] = None,
        stdin: Optional[bool] = None,
        stdin_once: Optional[bool] = None,
        termination_message_path: Optional[str] = None,
        termination_message_policy: Optional[str] = None,
        tty: Optional[bool] = None,
        volume_devices: Optional[List[VolumeDevice]] = None,
        volume_mounts: Optional[List[VolumeMount]] = None,
        working_dir: Optional[str] = None,
    ):
        self.args = args
        self.command = command
        self.env = env
        self.envFrom = env_from
        self.image = image
        self.imagePullPolicy = image_pull_policy
        self.lifecycle = lifecycle
        self.livenessProbe = liveness_probe
        self.name = name
        self.ports = ports
        self.readinessProbe = readiness_probe
        self.resources = resources
        self.securityContext = security_context
        self.startupProbe = startup_probe
        self.stdin = stdin
        self.stdinOnce = stdin_once
        self.terminationMessagePath = termination_message_path
        self.terminationMessagePolicy = termination_message_policy
        self.tty = tty
        self.volumeDevices = volume_devices
        self.volumeMounts = volume_mounts
        self.workingDir = working_dir


class ContainerImage(HelmYaml):
    """
    :param names:Names by which this image is known. e.g. \
        ["k8s.gcr.io/hyperkube:v1.0.7", \
        "dockerhub.io/google_containers/hyperkube:v1.0.7"]
    :type names: List[str]
    :param size_bytes:The size of the image in bytes.
    :type size_bytes: int
    """

    def __init__(self, names: List[str], size_bytes: int):
        self.names = names
        self.sizeBytes = size_bytes


class ContainerStateRunning(HelmYaml):
    """
    :param started_at:Time at which the container was last (re-)started
    :type started_at: time
    """

    def __init__(self, started_at: time):
        self.startedAt = started_at


class ContainerStateWaiting(HelmYaml):
    """
    :param message:Message regarding why the container is not yet running.
    :type message: str
    :param reason:(brief) reason the container is not yet running.
    :type reason: str
    """

    def __init__(self, message: str, reason: str):
        self.message = message
        self.reason = reason


class ContainerStateTerminated(HelmYaml):
    """
    :param container_id:Container's ID in the format 'docker://<container_id>'
    :type container_id: str
    :param exit_code:Exit status from the last termination of the container
    :type exit_code: int
    :param finished_at:Time at which the container last terminated
    :type finished_at: time
    :param message:Message regarding the last termination of the container
    :type message: str
    :param reason:(brief) reason from the last termination of the container
    :type reason: str
    :param signal:Signal from the last termination of the container
    :type signal: int
    :param started_at:Time at which previous execution of the container started
    :type started_at: time
    """

    def __init__(
        self,
        container_id: str,
        exit_code: int,
        finished_at: time,
        message: str,
        reason: str,
        signal: int,
        started_at: time,
    ):
        self.containerID = container_id
        self.exitCode = exit_code
        self.finishedAt = finished_at
        self.message = message
        self.reason = reason
        self.signal = signal
        self.startedAt = started_at


class ContainerState(HelmYaml):
    """
    :param running:Details about a running container
    :type running: ContainerStateRunning
    :param terminated:Details about a terminated container
    :type terminated: ContainerStateTerminated
    :param waiting:Details about a waiting container
    :type waiting: ContainerStateWaiting
    """

    def __init__(
        self,
        running: ContainerStateRunning,
        terminated: ContainerStateTerminated,
        waiting: ContainerStateWaiting,
    ):
        self.running = running
        self.terminated = terminated
        self.waiting = waiting
