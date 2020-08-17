# Avionix
Helm is a very useful tool that facilitates infrastructure releases to kubernetes. It's 
interface is written entirely in yaml which makes it hard to use and also has
 created a need for code to be repeated in many cases. The goal of avionix is to
  create an object oriented interface to make helm easy to use and reduce the
   repetition of code when possible.
   
# Documentation
The official documentation is can be found on ReadTheDocs: https://avionix.readthedocs.io/en/latest/index.html
   
# Requirements

In order for avionix to work you will need the following command line tools

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [helm](https://helm.sh/docs/intro/install/)
   
# Installation

```bash
pip install avionix
```

## Warnings

Note that you currently cannot use public instance variables when implementing a
 child class one of the kubernetes components.
 
For example in the above inheritance example code, this would break the helm output,

```python
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
```

However, instead using a variable 
```python
self._my_personal_variable
```
would not break the output.

# Examples

A good example of how avionix can be used is can be found in [avionix_airflow](https://github.com/zbrookle/avionix_airflow), which
 is airflow implemented on kubernetes using avionix