Warnings
========

Note that you currently cannot use public instance variables when implementing a
child class one of the kubernetes components.

For example in the provided :ref:`inheritance` example code, this would break the helm
output,

.. code-block:: python

    class WebserverUI(AirflowContainer):
        def __init__(
            self,
            sql_options: SqlOptions,
            redis_options: RedisOptions,
            airflow_options: AirflowOptions,
        ):
            self.my_personal_variable = "I'm breaking helm!"
            super().__init__(
                "webserver",
                sql_options,
                redis_options,
                airflow_options,
                ports=[ContainerPort(8080, host_port=8080)],
                readiness_probe=AvionixAirflowProbe("/airflow", 8080, "0.0.0.0"),
            )

However, instead using a variable

.. code-block:: python

    self._my_personal_variable

would not break the output.