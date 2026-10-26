#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v docker >/dev/null || { echo "Docker not installed. Install Docker Desktop with WSL integration."; exit 1; }
docker compose version >/dev/null
if [[ ! -f .env ]]; then cp .env.example .env; echo "Created .env; change default credentials for non-local use."; fi
docker compose up --build -d
docker compose ps
printf '\nUI: http://localhost:8080\nAPI: http://localhost:8000/docs\n'
