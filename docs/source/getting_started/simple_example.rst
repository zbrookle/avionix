Simple Example
==============

With avionix, you can build with the typical kubernetes components

For example for a deployment:

.. literalinclude:: ../../../examples/deployment_example.py
   :language: python

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