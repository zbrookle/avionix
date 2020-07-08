from typing import List, Optional

from helm_factory.yaml.yaml_handling import HelmYaml


class HTTPHeader(HelmYaml):
    """
    :param value: The header field value
    :param name: The header field name
    """

    def __init__(self, value: str, name: Optional[str] = None):
        self.value = value
        self.name = name


class HTTPGetAction(HelmYaml):
    """
    :param http_headers: Custom headers to set in the request. HTTP allows repeated \
        headers.
    :param path: Path to access on the HTTP server.
    :param port: Name or number of the port to access on the container. Number must be \
        in the range 1 to 65535. Name must be an IANA_SVC_NAME.
    :param host: Host name to connect to, defaults to the pod IP. You probably want to \
        set "Host" in httpHeaders instead.
    :param scheme: Scheme to use for connecting to the host. Defaults to HTTP.
    """

    def __init__(
        self,
        http_headers: List[HTTPHeader],
        path: str,
        port: str,
        host: Optional[str] = None,
        scheme: Optional[str] = None,
    ):
        self.httpHeaders = http_headers
        self.path = path
        self.port = port
        self.host = host
        self.scheme = scheme


class ExecAction(HelmYaml):
    """
    :param command: Command is the command line to execute inside the container, the \
        working directory for the command  is root ('/') in the container's \
        filesystem. The command is simply exec'd, it is not run inside a shell, so \
        traditional shell instructions ('|', etc) won't work. To use a shell, you need \
        to explicitly call out to that shell. Exit status of 0 is treated as \
        live/healthy and non-zero is unhealthy.
    """

    def __init__(self, command: List[str]):
        self.command = command


class TCPSocketAction(HelmYaml):
    """
    :param port: Number or name of the port to access on the container. Number must be \
        in the range 1 to 65535. Name must be an IANA_SVC_NAME.
    :param host: Optional: Host name to connect to, defaults to the pod IP.
    """

    def __init__(self, port: str, host: Optional[str] = None):
        self.port = port
        self.host = host


class Probe(HelmYaml):
    """
    :param exec: One and only one of the following should be specified. Exec specifies \
        the action to take.
    :param http_get: HTTPGet specifies the http request to perform.
    :param initial_delay_seconds: Number of seconds after the container has started \
        before liveness probes are initiated. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    :param period_seconds: How often (in seconds) to perform the probe. Default to 10 \
        seconds. Minimum value is 1.
    :param tcp_socket: TCPSocket specifies an action involving a TCP port. TCP hooks \
        not yet supported
    :param failure_threshold: Minimum consecutive failures for the probe to be \
        considered failed after having succeeded. Defaults to 3. Minimum value is 1.
    :param success_threshold: Minimum consecutive successes for the probe to be \
        considered successful after having failed. Defaults to 1. Must be 1 for \
        liveness and startup. Minimum value is 1.
    :param timeout_seconds: Number of seconds after which the probe times out. \
        Defaults to 1 second. Minimum value is 1. More info: \
        https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle#container-probes  # noqa
    """

    def __init__(
        self,
        exec: ExecAction,
        http_get: HTTPGetAction,
        initial_delay_seconds: int,
        period_seconds: int,
        tcp_socket: TCPSocketAction,
        failure_threshold: Optional[int] = None,
        success_threshold: Optional[int] = None,
        timeout_seconds: Optional[int] = None,
    ):
        self.exec = exec
        self.httpGet = http_get
        self.initialDelaySeconds = initial_delay_seconds
        self.periodSeconds = period_seconds
        self.tcpSocket = tcp_socket
        self.failureThreshold = failure_threshold
        self.successThreshold = success_threshold
        self.timeoutSeconds = timeout_seconds


class Handler(HelmYaml):
    """
    :param exec: One and only one of the following should be specified. Exec specifies \
        the action to take.
    :param http_get: HTTPGet specifies the http request to perform.
    :param tcp_socket: TCPSocket specifies an action involving a TCP port. TCP hooks \
        not yet supported
    """

    def __init__(
        self, exec: ExecAction, http_get: HTTPGetAction, tcp_socket: TCPSocketAction
    ):
        self.exec = exec
        self.httpGet = http_get
        self.tcpSocket = tcp_socket


class Lifecycle(HelmYaml):
    """
    :param post_start: PostStart is called immediately after a container is created. \
        If the handler fails, the container is terminated and restarted according to \
        its restart policy. Other management of the container blocks until the hook \
        completes. More info: \
        https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks  # noqa
    :param pre_stop: PreStop is called immediately before a container is terminated \
        due to an API request or management event such as liveness/startup probe \
        failure, preemption, resource contention, etc. The handler is not called if \
        the container crashes or exits. The reason for termination is passed to the \
        handler. The Pod's termination grace period countdown begins before the \
        PreStop hooked is executed. Regardless of the outcome of the handler, the \
        container will eventually terminate within the Pod's termination grace period. \
        Other management of the container blocks until the hook completes or until the \
        termination grace period is reached. More info: \
        https://kubernetes.io/docs/concepts/containers/container-lifecycle-hooks/#container-hooks  # noqa
    """

    def __init__(self, post_start: Handler, pre_stop: Handler):
        self.postStart = post_start
        self.preStop = pre_stop
