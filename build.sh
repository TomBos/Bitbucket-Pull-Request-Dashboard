#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
VITE_DIR="$SRC_DIR/vite"


pnpm --prefix vite install
pnpm --prefix vite build && mv "$VITE_DIR"/dist/* "$SRC_DIR/public/"

rm -r "$VITE_DIR/dist"

python3 http_server.py


