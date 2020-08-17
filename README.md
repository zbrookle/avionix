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

# Examples

A good example of how avionix can be used is can be found in [avionix_airflow](https://github.com/zbrookle/avionix_airflow), which
 is airflow implemented on kubernetes using avionix