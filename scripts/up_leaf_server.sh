#!/usr/bin/env bash
set -euo pipefail

docker compose -f compose.leaf-server.yml up -d
