Simple Example
==============

With avionix, you can build with the typical kubernetes components

For example for a deployment:

.. code-block:: python

    from avionix import ChartBuilder, ChartInfo, ObjectMeta
    from avionix.kube.core import (
        PodSpec,
        LabelSelector,
        Container,
        ContainerPort,
        EnvVar,
    )
    from avionix.kube.apps import Deployment, DeploymentSpec, PodTemplateSpec

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

from there you either do

.. code-block:: python

    builder.install_chart()

if you want to install the chart directly and let avionix handle it or you can use

.. code-block:: python

    builder.generate_chart()

to generate the chart and template yaml files

Additionally

.. code-block:: python

    builder.uninstall_chart()

and

.. code-block:: python

    builder.upgrade_chart()

are included.

For more specifics about chart builder see the :ref:`chart` documentation.

These are all directly equivalent to their corresponding helm commands and also
 support passing in command line by passing a dictionary in with the options needed.

For example,

.. code-block:: python

    builder.install_chart(options={"create-namespace": None, "dependency-update": None}))


If a command line option takes an argument in helm, then that value should be given
 as the value in the corresponding dictionary key in the options dictionary.