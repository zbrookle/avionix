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

    helm repo add stable https://charts.helm.sh/stable
    helm install <path_to_my_chart> --dependency-update

This will generate a directory with the following structure:

.. code-block:: bash

    my_chart/
    ├── Chart.yaml
    ├── charts
    │   └── grafana-5.5.2.tgz
    |   └── local-chart-0.1.0.tgz
    ├── templates
    └── values.yaml

The *Chart.yaml* will be:

.. code-block:: yaml

    apiVersion: 3.2.4
    appVersion: v1
    dependencies:
    - name: grafana
      repository: https://charts.helm.sh/stable
      version: 5.5.2
    - name: local-chart
      repository: file:///path/to/my/local-chart
      version: 0.1.0
    name: my_chart
    version: 0.1.0

The *values.yaml* will be:

.. code-block:: yaml

    grafana:
        resources:
            requests:
                memory: 100Mi

*templates* is empty in this case because there are no kubernetes objects added to the builder.

*charts* will contain the zipped external charts that you've included as dependencies.
    
Note that the parameters are slightly different for installing a local chart, it must be marked as local
and the repo uri must be *file://* followed by the absolute path to the chart folder.