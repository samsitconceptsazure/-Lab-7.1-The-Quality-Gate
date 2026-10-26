# Lab 7.2 — Docker Build Gate

## Goal
Test first, then build API and web Docker images. This folder contains a **complete standalone copy** of the React UI, FastAPI backend, PostgreSQL Compose database, tests, Dockerfiles, infrastructure examples, and the Lab 7.2 GitHub workflow. No files from another lab folder are needed.

## Recommended platform
**WSL2 Ubuntu + Docker Desktop with WSL integration.** No AWS account or charges are required for the application and GitHub Actions exercises. AWS EKS is optional for advanced deployment in Lab 7.5.

## Prerequisites (per lab)
- WSL2 Ubuntu, Docker Desktop with WSL integration enabled, Docker Compose, Git, curl, Python 3 for JSON formatting.
- Ports 8080 and 8000 available.
- For GitHub CI: a GitHub repository containing **this lab folder as the repository root**. Use a separate repository per stage or replace the files in the same teaching repository between stages; never push the five parent folders as a single repository and expect their nested workflows to run.

## Step 1 — Enter only this lab folder
```bash
cd 7.2
ls -la
```
Expected: `backend/`, `frontend/`, `docker-compose.yml`, `.github/workflows/`, `scripts/`, `k8s/`, `gitops/`, and `05_MERMAID_DIAGRAMS.md`.

## Step 2 — Deploy the entire application
```bash
bash scripts/deploy.sh
```
Sample output:
```text
[+] Running 4/4
 ✔ Network ... created
 ✔ Container ...-db-1 Healthy
 ✔ Container ...-api-1 Started
 ✔ Container ...-web-1 Started
UI: http://localhost:8080
API: http://localhost:8000/docs
```

## Step 3 — Validate application and API
```bash
bash scripts/test.sh
```
Sample output (illustrative):
```text
=== Health ===
{"status":"healthy","service":"retailops-api"}
=== Readiness ===
{"status":"ready","database":"connected"}
=== Products ===
[{"id":1,"sku":"SKU-1001","name":"Wireless Barcode Scanner",...}]
=== API tests ===
........
8 passed in ...
```
Open **http://localhost:8080** to inspect the enterprise dashboard and **http://localhost:8000/docs** for Swagger. Login credentials are in `.env.example` and must be changed outside localhost demos.

## Step 4 — Test authentication and orders
```bash
curl -s http://localhost:8000/api/products
curl -s http://localhost:8000/api/auth/login -H 'Content-Type: application/json' \
  -d '{"username":"admin","password":"ChangeMe_Admin_123!"}'
```
Sample login response (token shortened):
```json
{"access_token":"eyJ...","token_type":"bearer","role":"admin"}
```
Try placing an order in the UI. Confirm stock decreases, and verify a customer cannot update stock (`403 Forbidden`).

## Step 5 — Push this standalone lab to GitHub
```bash
git init
git branch -M main
git add .
git commit -m "lab 7.2: Docker Build Gate"
git remote add origin https://github.com/YOUR_USER/retailops-lab-7-2.git
git push -u origin main
```
Create the empty GitHub repository first. If Git is already configured, skip duplicate initialization/remote steps. `.env` is ignored.

## Step 6 — Run the stage-specific GitHub Actions workflow
Open GitHub Actions → Lab 7.2 - Docker Build Gate → Run workflow on main.

**Expected evidence:** test job succeeded and build job succeeded.


## Step 7 — Troubleshooting
```bash
docker compose ps
docker compose logs --tail=80 api
docker compose logs --tail=80 db
docker compose logs --tail=80 web
```
- If Docker cannot connect, start Docker Desktop and enable WSL integration.
- If ports are in use, stop the conflicting service or edit Compose ports.
- If login fails after changing `.env`, remember seeded users persist in the PostgreSQL volume.
- Checkov or Trivy may report real security findings; do not bypass the security gates.

## Step 8 — Stop and clean up
```bash
bash scripts/destroy.sh
```
This retains the database volume. `docker compose down -v` deletes local lab data.

## Five diagrams
See **`05_MERMAID_DIAGRAMS.md`** for five diagrams included directly in this folder.

## Progressive learning
Each lab is a complete runnable snapshot; stage 7.2 focuses on its new security/delivery control while retaining the same realistic application. All GitHub Actions stages are intentionally separated to make teaching and evidence capture easier.
