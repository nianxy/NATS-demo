#!/usr/bin/env bash
set -euo pipefail

docker compose -f compose.hub-server.yml down --remove-orphans
docker compose -f compose.leaf-server.yml down --remove-orphans
