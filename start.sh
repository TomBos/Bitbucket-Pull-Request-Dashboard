#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

python "$SCRIPT_DIR/src/http_server.py"

