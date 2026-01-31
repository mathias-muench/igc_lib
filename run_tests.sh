#!/bin/bash
set -e

echo "Running tests with python3"
if [ -z "$1" ]; then
    # No argument provided - run all tests
    /usr/bin/env python3 -m unittest discover -t src -s src/igc_lib/
else
    /usr/bin/env python3 -m unittest $1
fi
