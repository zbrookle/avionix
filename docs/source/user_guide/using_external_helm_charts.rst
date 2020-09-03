Using External Helm Charts
==========================

External helm charts can be included by placing them in the dependencies parameter of
the :any:`ChartInfo` object that must be passed to :any:`ChartBuilder`.
Additionally, the values that would normally be passed to the chart dependency in
*values.yaml* can be passed in the :any:`ChartDependency` object's *values* parameter.

For example, this is how you could use the
`Grafana helm chart <https://hub.helm.sh/charts/stable/grafana>`_:

.. literalinclude:: ../../../examples/external_helm_charts_example.py
   :language: python

In this simple example, the following helm commands will be run after building the
chart:

.. code-block:: bash

    helm repo add stable https://kubernetes-charts.storage.googleapis.com/
    helm install <path_to_my_chart> --dependency-update

The *values.yaml* will end up as:

.. code-block:: yaml

    grafana:
        resources:
            requests:
                memory: 100Mi
