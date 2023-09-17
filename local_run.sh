#!/bin/bash
# shellcheck shell=bash

PATH_TO_TEST=tests/test_ad_placement_positions.py
TEST_CASE_NAME=""
DURATIONS=0
VERBOSE=10
if [ "$TEST_CASE_NAME" = "" ]; then
  python -m pytest -s --verbose --durations=$DURATIONS -vv -n $VERBOSE --reruns 1 --reruns-delay 5
else
  python -m pytest $PATH_TO_TEST::$TEST_CASE_NAME -s --verbose
fi
