#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
command -v docker >/dev/null || { echo "Docker is required"; exit 1; }
docker info >/dev/null
if [[ ! -f .env ]]; then cp .env.example .env; echo "Created .env from .env.example; review credentials before continuing."; fi
docker compose up --build -d
echo "Waiting for API health..."
for i in $(seq 1 30); do
  if curl -fsS http://localhost:8000/health >/dev/null; then break; fi
  sleep 2
done
curl -fsS http://localhost:8000/health
echo
curl -fsS http://localhost:8000/ready
echo
docker compose exec -T api pytest -q
echo "Local build and API tests completed."
