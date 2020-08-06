#!/bin/bash -e

pytest --log-cli-level info --log-format "[%(filename)s:%(lineno)s] %(message)s"