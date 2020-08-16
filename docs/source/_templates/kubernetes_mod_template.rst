{% extends "!autosummary/module.rst" %}

{% block classes %}
{% if classes %}
{% for item in classes %}
  .. autoclass:: {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}