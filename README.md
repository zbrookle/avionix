# Avionix
Helm is a very useful tool that facilitates infrastructure releases to kubernetes. It's 
interface is written entirely in yaml which makes it hard to use and also has
 created a need for code to be repeated in many cases. The goal of avionix is to
  create an object oriented interface to make helm easy to use and reduce the
   repetition of code when possible.
   
# Installation

```bash
pip install avionix
```

# Usage

With avionix you can, build with the typical kubernetes components

## Simple Example

For example for a deployment:
```python
from avionix import ChartBuilder, ChartInfo, ObjectMeta
from avionix.kubernetes_objects.core import (
    PodSpec,
    LabelSelector,
    Container,
    ContainerPort,
    EnvVar,
)
from avionix.kubernetes_objects.apps import Deployment, DeploymentSpec, PodTemplateSpec

container = Container(
    name=f"test-container",
    image="k8s.gcr.io/echoserver:1.4",
    env=[EnvVar("test", "test-value")],
    ports=[ContainerPort(8080)],
)

deployment = Deployment(
    metadata=ObjectMeta(name=f"test-deployment", labels={"app": "my_app"}),
    spec=DeploymentSpec(
        replicas=1,
        template=PodTemplateSpec(
            ObjectMeta(labels={"app": "my_app"}),
            spec=PodSpec(containers=[container]),
        ),
        selector=LabelSelector(match_labels={"app": "my_app"}),
    ),
)

builder = ChartBuilder(
    ChartInfo(api_version="3.2.4", name="test", version="0.1.0", app_version="v1"),
    [deployment],
)
```
from there you either do 
```python
builder.install_chart()
```
if you want to install the chart directly and let avionix handle it
or
you can use 
```python
builder.generate_chart()
```
to view the chart.

Additionally there are methods for upgrade and uninstall charts.
These are all directly equivalent to the helm commands.

## Inheritance

The real power of avionix comes from it being object oriented. The one thing that
 helm is missing that avionix has is inheritance.
```python

```

# Development Environmnent

For development you will need
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) 
- [helm](https://helm.sh/docs/intro/install/)
- [docker](https://docs.docker.com/get-docker/)

# Starting the development environment

Be sure that docker is running, then run the following command
```bash
minikube start --driver=docker
```

## Warnings

Note that you currently cannot use public variables if subclassing one of the
 kubernetes components.