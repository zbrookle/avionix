
# Avionix

![CI](https://github.com/zbrookle/avionix/workflows/CI/badge.svg)
[![Downloads](https://pepy.tech/badge/avionix)](https://pepy.tech/project/avionix)
[![PyPI license](https://img.shields.io/pypi/l/avionix.svg)](https://github.com/zbrookle/avionix/blob/master/LICENSE.txt)
[![PyPI status](https://img.shields.io/pypi/status/avionix.svg)](https://pypi.python.org/pypi/avionix/)
[![PyPI version shields.io](https://img.shields.io/pypi/v/avionix.svg)](https://pypi.python.org/pypi/avionix/)
[![codecov](https://codecov.io/gh/zbrookle/avionix/branch/master/graph/badge.svg)](https://codecov.io/gh/zbrookle/avionix)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is avionix?

Helm is a very useful tool that facilitates infrastructure releases to kubernetes. It's 
interface is written entirely in yaml which makes it hard to use and also has
created a need for code to be repeated in many cases. The goal of **avionix** is to
provide an object oriented interface to make helm easy to use and reduce the
repetition of code when possible.
   
## Documentation

The official documentation is can be found on ReadTheDocs: https://avionix.readthedocs.io/en/latest/index.html
   
## Requirements

In order for avionix to work you will need the following command line tools

- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [helm](https://helm.sh/docs/intro/install/)
   
## Installation

```bash
pip install avionix
```

## Examples

A good example of how avionix can be used is can be found in [avionix_airflow](https://github.com/zbrookle/avionix_airflow), which
 is airflow implemented on kubernetes using avionix