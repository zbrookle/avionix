from helm_factory.yaml.yaml_handling import HelmYaml


class LoadBalancerIngress(HelmYaml):
    """
    :param hostname: Hostname is set for load-balancer ingress points that are DNS \
        based (typically AWS load-balancers)
    :param ip: IP is set for load-balancer ingress points that are IP based (typically \
        GCE or OpenStack load-balancers)
    """

    def __init__(self, hostname: str, ip: str):
        self.hostname = hostname
        self.ip = ip
