#!/bin/bash
#
# Run checks related to code quality.
#
# This script is intended for both the CI and to check locally that code standards are
# respected. We are currently linting (PEP-8 and similar), looking for patterns of
# common mistakes (sphinx directives with missing blank lines, old style classes,
# unwanted imports...), we run doctests here (currently some files only), and we
# validate formatting error in docstrings.
#
# Usage:
#   $ ./ci/code_checks.sh               # run all checks
#   $ ./ci/code_checks.sh lint          # run linting only
#   $ ./ci/code_checks.sh patterns      # check for patterns that should not exist
#   $ ./ci/code_checks.sh code          # checks on imported code
#   $ ./ci/code_checks.sh doctests      # run doctests
#   $ ./ci/code_checks.sh docstrings    # validate docstring errors
#   $ ./ci/code_checks.sh dependencies  # check that dependencies are consistent
#   $ ./ci/code_checks.sh typing	# run static type analysis

[[ -z "$1" || "$1" == "lint" || "$1" == "patterns" || "$1" == "code" || "$1" == "doctests" || "$1" == "docstrings" || "$1" == "dependencies" || "$1" == "typing" ]] || \
    { echo "Unknown command $1. Usage: $0 [lint|patterns|code|doctests|docstrings|dependencies|typing]"; exit 9999; }

RET=0
CHECK=$1


if [[ "$GITHUB_ACTIONS" == "true" ]]; then
    FLAKE8_FORMAT="##[error]%(path)s:%(row)s:%(col)s:%(code)s:%(text)s"
    INVGREP_PREPEND="##[error]"
else
    FLAKE8_FORMAT="default"
fi

### LINTING ###
if [[ -z "$CHECK" || "$CHECK" == "lint" ]]; then

    echo "black --version"
    black --version

    MSG='Checking black formatting' ; echo $MSG
    black . --check
    RET=$(($RET + $?)) ; echo $MSG "DONE"

    # `setup.cfg` contains the list of error codes that are being ignored in flake8

    echo "flake8 --version"
    flake8 --version

    MSG='Linting .py code' ; echo $MSG
    flake8 --format="$FLAKE8_FORMAT" .
    RET=$(($RET + $?)) ; echo $MSG "DONE"

    echo "isort --version-number"
    isort --version-number

    # Imports - Check formatting using isort see setup.cfg for settings
    MSG='Check import format using isort' ; echo $MSG
    ISORT_CMD="isort --recursive --check-only sql_to_ibis"
    if [[ "$GITHUB_ACTIONS" == "true" ]]; then
        eval $ISORT_CMD | awk '{print "##[error]" $0}'; RET=$(($RET + ${PIPESTATUS[0]}))
    else
        eval $ISORT_CMD
    fi
    RET=$(($RET + $?)) ; echo $MSG "DONE"

fi

### PATTERNS ###
if [[ -z "$CHECK" || "$CHECK" == "patterns" ]]; then

  python ci/pattern_checker.py

fi

### TYPING ###
if [[ -z "$CHECK" || "$CHECK" == "typing" ]]; then

    echo "mypy --version"
    mypy --version

    MSG='Performing static analysis using mypy' ; echo $MSG
    mypy sql_to_ibis
    RET=$(($RET + $?)) ; echo $MSG "DONE"
fi


exit $RET