#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
docker compose down
echo 'Stopped; PostgreSQL named volume retained. To delete data explicitly: docker compose down -v'
