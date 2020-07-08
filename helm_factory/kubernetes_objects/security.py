from typing import List, Optional

from helm_factory.yaml.yaml_handling import HelmYaml


class WindowsSecurityContextOptions(HelmYaml):
    """
    :param gmsa_credential_spec: GMSACredentialSpec is where the GMSA admission \
        webhook (https://github.com/kubernetes-sigs/windows-gmsa) inlines the contents \
        of the GMSA credential spec named by the GMSACredentialSpecName field.
    :param gmsa_credential_spec_name: GMSACredentialSpecName is the name of the GMSA \
        credential spec to use.
    :param run_as_user_name: The UserName in Windows to run the entrypoint of the \
        container process. Defaults to the user specified in image metadata if \
        unspecified. May also be set in PodSecurityContext. If set in both \
        SecurityContext and PodSecurityContext, the value specified in SecurityContext \
        takes precedence.
    """

    def __init__(
        self,
        gmsa_credential_spec: str,
        gmsa_credential_spec_name: str,
        run_as_user_name: Optional[str] = None,
    ):
        self.gmsaCredentialSpec = gmsa_credential_spec
        self.gmsaCredentialSpecName = gmsa_credential_spec_name
        self.runAsUserName = run_as_user_name


class SELinuxOptions(HelmYaml):
    """
    :param level: Level is SELinux level label that applies to the container.
    :param role: Role is a SELinux role label that applies to the container.
    :param type: Type is a SELinux type label that applies to the container.
    :param user: User is a SELinux user label that applies to the container.
    """

    def __init__(self, level: str, role: str, type: str, user: str):
        self.level = level
        self.role = role
        self.type = type
        self.user = user


class Capabilities(HelmYaml):
    """
    :param add: Added capabilities
    :param drop: Removed capabilities
    """

    def __init__(self, add: List[str], drop: List[str]):
        self.add = add
        self.drop = drop


class SecurityContext(HelmYaml):
    """
    :param allow_privilege_escalation: AllowPrivilegeEscalation controls whether a \
        process can gain more privileges than its parent process. This bool directly \
        controls if the no_new_privs flag will be set on the container process. \
        AllowPrivilegeEscalation is true always when the container is: 1) run as \
        Privileged 2) has CAP_SYS_ADMIN
    :param run_as_group: The GID to run the entrypoint of the container process. Uses \
        runtime default if unset. May also be set in PodSecurityContext.  If set in \
        both SecurityContext and PodSecurityContext, the value specified in \
        SecurityContext takes precedence.
    :param run_as_non_root: Indicates that the container must run as a non-root user. \
        If true, the Kubelet will validate the image at runtime to ensure that it does \
        not run as UID 0 (root) and fail to start the container if it does. If unset \
        or false, no such validation will be performed. May also be set in \
        PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, \
        the value specified in SecurityContext takes precedence.
    :param se_linux_options: The SELinux context to be applied to the container. If \
        unspecified, the container runtime will allocate a random SELinux context for \
        each container.  May also be set in PodSecurityContext.  If set in both \
        SecurityContext and PodSecurityContext, the value specified in SecurityContext \
        takes precedence.
    :param windows_options: The Windows specific settings applied to all containers. \
        If unspecified, the options from the PodSecurityContext will be used. If set \
        in both SecurityContext and PodSecurityContext, the value specified in \
        SecurityContext takes precedence.
    :param capabilities: The capabilities to add/drop when running containers. \
        Defaults to the default set of capabilities granted by the container runtime.
    :param privileged: Run container in privileged mode. Processes in privileged \
        containers are essentially equivalent to root on the host. Defaults to false.
    :param proc_mount: procMount denotes the type of proc mount to use for the \
        containers. The default is DefaultProcMount which uses the container runtime \
        defaults for readonly paths and masked paths. This requires the ProcMountType \
        feature flag to be enabled.
    :param read_only_root_filesystem: Whether this container has a read-only root \
        filesystem. Default is false.
    :param run_as_user: The UID to run the entrypoint of the container process. \
        Defaults to user specified in image metadata if unspecified. May also be set \
        in PodSecurityContext.  If set in both SecurityContext and PodSecurityContext, \
        the value specified in SecurityContext takes precedence.
    """

    def __init__(
        self,
        allow_privilege_escalation: bool,
        run_as_group: int,
        run_as_non_root: bool,
        se_linux_options: SELinuxOptions,
        windows_options: WindowsSecurityContextOptions,
        capabilities: Optional[Capabilities] = None,
        privileged: Optional[bool] = None,
        proc_mount: Optional[str] = None,
        read_only_root_filesystem: Optional[bool] = None,
        run_as_user: Optional[int] = None,
    ):
        self.allowPrivilegeEscalation = allow_privilege_escalation
        self.runAsGroup = run_as_group
        self.runAsNonRoot = run_as_non_root
        self.seLinuxOptions = se_linux_options
        self.windowsOptions = windows_options
        self.capabilities = capabilities
        self.privileged = privileged
        self.procMount = proc_mount
        self.readOnlyRootFilesystem = read_only_root_filesystem
        self.runAsUser = run_as_user
