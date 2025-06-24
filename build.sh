#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
VITE_DIR="$SCRIPT_DIR/vite"
PUBLIC_DIR="$SCRIPT_DIR/public/"


if [[ ! -d "$VITE_DIR" ]]; then
  mkdir -p "$VITE_DIR"
fi

if [[ ! -d "$PUBLIC_DIR" ]]; then
  mkdir -p "$PUBLIC_DIR"
fi

rm -r "$PUBLIC_DIR"*

pnpm --prefix vite install && pnpm --prefix vite build

mv -f "$VITE_DIR"/dist/* "$PUBLIC_DIR"
rm -r "$VITE_DIR/dist"

python3 http_server.py


