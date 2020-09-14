Writing to (or Reading from) *values.yaml*
==========================================

``avionix`` supports the use of helm's *values.yaml* file for creating an
interface for others to pass values to published helm charts. Avionix has objects
that must be used in order to interact with and change the *values.yaml* file.
These objects are the :any:`Value` object and the :any:`Values` object. Values contains
the values that you would normally put in a *values.yaml*, but in a Python
dictionary format and :any:`Value` is a value that is referencing the *values.yaml*
file. :any:`Value` takes one parameter which is a string that uses dot notation to
specify the value to use from *values.yaml*.

For example:

.. literalinclude:: ../../../examples/using_values_yaml.py
   :language: python

For more information on *values.yaml* see the helm documentation
`here <https://helm.sh/docs/chart_template_guide/values_files/>`__


