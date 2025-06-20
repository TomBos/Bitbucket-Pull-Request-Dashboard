#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
SRC_DIR="$SCRIPT_DIR/src"
VITE_DIR="$SRC_DIR/vite"


pnpm --prefix src/vite install
pnpm --prefix src/vite build && mv "$VITE_DIR"/dist/* "$SRC_DIR/public/"

rm -r "$VITE_DIR/dist"

python3 "$SRC_DIR/http_server.py"