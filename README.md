# Avionix
Helm is a very useful tool that facilitates infrastructure releases to kubernetes. It's 
interface is written entirely in yaml which makes it hard to use and also has
 created a need for code to be repeated in many cases. The goal of avionix is to
  create an object oriented interface to make helm easy to use and reduce the
   repetition of code when possible.
   
# Installation

```bash
pip install avionix
```

# Development Environmnent

For development you will need
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [minikube](https://kubernetes.io/docs/tasks/tools/install-minikube/) 
- [helm](https://helm.sh/docs/intro/install/)
- [docker](https://docs.docker.com/get-docker/)

# Starting the development environment

Be sure that docker is running, then run the following command
```bash
minikube start --driver=docker
```
