#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
echo '=== Health ==='
curl -fsS http://localhost:8000/health; echo
echo '=== Readiness ==='
curl -fsS http://localhost:8000/ready; echo
echo '=== Products ==='
curl -fsS http://localhost:8000/api/products | python3 -m json.tool | head -35
echo '=== API tests ==='
docker compose exec -T api pytest -q
