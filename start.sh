#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"

pnpm --prefix="$SCRIPT_DIR/backend" run dev

