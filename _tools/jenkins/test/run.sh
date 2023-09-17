#!/bin/bash
# shellcheck shell=bash

python -m pytest -s --verbose --durations=0 -vv -n 10 --reruns 1 --reruns-delay 5 --timeout=1500 --color=yes --junitxml test_results.xml
