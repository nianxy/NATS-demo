#!/usr/bin/env bash
set -euo pipefail

docker compose -f compose.hub-server.yml up -d
