#!/bin/bash -e

export SHELL=/bin/bash
pytest --log-cli-level info --log-format "[%(filename)s:%(lineno)s] %(message)s"