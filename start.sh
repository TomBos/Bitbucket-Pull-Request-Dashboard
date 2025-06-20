#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
SRC_DIR="$SCRIPT_DIR/src"
VITE_DIR="$SRC_DIR/vite"

echo "$VITE_DIR"