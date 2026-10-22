# RetailOps DevSecOps Labs 7.1–7.5
## Step-by-Step Lab Manual with Commands and Sample Outputs

**Application:** RetailOps Enterprise Order Management  
**Stack:** React + Vite, FastAPI, PostgreSQL, JWT/RBAC, Docker, GitHub Actions, Checkov, Trivy, GHCR, Kubernetes, Argo CD.

> **Sample-output note:** Outputs below are illustrative examples. Versions, test counts, image IDs, Git commit SHAs, Checkov findings, Trivy findings, and Kubernetes resource names can vary. Use the actual command output in your environment as the source of truth.

---

## 1. Lab objectives

By completing this lab, you will:

1. Run a realistic order-management application locally.
2. Validate login, JWT authentication, role-based authorization, orders, and inventory.
3. Run API tests and build the React frontend.
4. Run the five GitHub Actions stages separately without recreating the project.
5. Scan Terraform/Kubernetes configuration with Checkov.
6. Build Docker images, scan them with Trivy, and publish SHA-tagged images to GHCR.
7. Prepare Kubernetes manifests and configure Argo CD to reconcile desired state from Git.

## 2. Architecture and request flow

```mermaid
flowchart LR
    Browser[Browser] --> Web[React + Nginx]
    Web --> API[FastAPI REST API]
    API --> Auth[JWT + role checks]
    API --> DB[(PostgreSQL)]
    API --> Orders[Order processing]
    Orders --> Stock[Inventory validation]
    Stock --> DB
    Repo[GitHub repository] --> Actions[GitHub Actions]
    Actions --> Checkov[Checkov IaC scan]
    Checkov --> Docker[Build images]
    Docker --> Trivy[Trivy image scan]
    Trivy --> GHCR[GHCR SHA-tagged images]
    Repo --> Argo[Argo CD]
    GHCR --> K8s[Kubernetes workloads]
    Argo --> K8s
```

## 3. Prerequisites

Install or have access to:

- Docker Desktop or Docker Engine with the Docker Compose plugin
- Git
- A GitHub account and repository
- `curl` and a terminal
- For later deployment: `kubectl`, a Kubernetes cluster, Argo CD, and a PostgreSQL endpoint reachable from the cluster

Check tools:

```bash
docker --version
docker compose version
git --version
curl --version
```

Example output:

```text
Docker version 27.x.x, build ...
Docker Compose version v2.x.x
git version 2.x.x
curl 8.x.x (...)
```

Tool versions may differ.

## 4. Extract and inspect the project

Download and extract `retailops-devsecops-labs-7.1-to-7.5-complete.zip`, then enter the extracted directory.

```bash
cd retailops-devsecops-labs-7.1-to-7.5
ls
```

Expected key files/directories:

```text
README.md
.env.example
docker-compose.yml
backend/
frontend/
terraform/
k8s/
gitops/
scripts/
docs/
.github/workflows/
```

Check that all five workflows are present:

```bash
ls .github/workflows
```

Example:

```text
lab-7.1-quality.yml
lab-7.2-build.yml
lab-7.3-checkov.yml
lab-7.4-release.yml
lab-7.5-zero-trust.yml
```

Do not create a second project for each stage. All stages use this same repository.

## 5. One-time local configuration

Create the local environment file:

```bash
cp .env.example .env
```

Open `.env` and change the demo passwords and `JWT_SECRET_KEY` before sharing the environment. The values in `.env.example` are only for local training. Do not commit `.env`.

Start the application:

```bash
docker compose up --build -d
```

Example output (abbreviated):

```text
[+] Building ...
[+] Running 4/4
 ✔ Network ..._retailops Created
 ✔ Container ...-db-1    Healthy
 ✔ Container ...-api-1   Started
 ✔ Container ...-web-1   Started
```

Check the services:

```bash
docker compose ps
```

Example:

```text
NAME                 IMAGE              SERVICE   STATUS
...-db-1             postgres:16-alpine db        Up (healthy)
...-api-1            ...-api             api       Up
...-web-1            ...-web             web       Up
```

If a service is not healthy, inspect logs:

```bash
docker compose logs --tail=100 db
docker compose logs --tail=100 api
docker compose logs --tail=100 web
```

## 6. Verify the application

### 6.1 Open the UI and API docs

- UI: `http://localhost:8080`
- FastAPI Swagger UI: `http://localhost:8000/docs`
- Health: `http://localhost:8000/health`
- Readiness: `http://localhost:8000/ready`

### 6.2 Test health endpoints

```bash
curl -i http://localhost:8000/health
curl -i http://localhost:8000/ready
```

Sample output:

```http
HTTP/1.1 200 OK
content-type: application/json

{"status":"healthy","service":"retailops-api"}
```

Readiness example:

```json
{"status":"ready","database":"connected"}
```

### 6.3 List products

```bash
curl -s http://localhost:8000/api/products
```

Sample output (shortened):

```json
[
  {
    "id": 1,
    "sku": "SKU-1001",
    "name": "Wireless Barcode Scanner",
    "description": "USB/Bluetooth warehouse scanner",
    "price": 89.99,
    "stock": 35
  },
  {
    "id": 2,
    "sku": "SKU-1002",
    "name": "Thermal Shipping Labels",
    "description": "Roll of 500 shipping labels",
    "price": 18.5,
    "stock": 120
  }
]
```

The app seeds sample products and demo accounts when it starts against an empty database.

## 7. Test JWT login and role-based access

### 7.1 Obtain a customer token

The default local demo credentials are in `.env.example`. This example uses the default customer password; if you changed it, use your new value.

```bash
CUSTOMER_TOKEN=$(curl -s http://localhost:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"customer","password":"ChangeMe_Customer_123!"}' \
  | python -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')

echo "$CUSTOMER_TOKEN" | cut -c1-32
```

Sample output:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6Ik...
```

Do not paste real tokens into public logs or commit them to Git.

### 7.2 Verify current identity

```bash
curl -s http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
```

Sample:

```json
{"username":"customer","role":"customer"}
```

### 7.3 Confirm a customer cannot update stock

Use the first product ID returned by `/api/products`:

```bash
curl -i -X PATCH \
  "http://localhost:8000/api/products/1/stock?stock=999" \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
```

Expected sample:

```http
HTTP/1.1 403 Forbidden
{"detail":"Insufficient role"}
```

This demonstrates server-side role enforcement. Hiding buttons in the UI is not a substitute for API authorization.

### 7.4 Place an order

```bash
curl -s -X POST http://localhost:8000/api/orders \
  -H "Authorization: Bearer $CUSTOMER_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"items":[{"product_id":1,"quantity":2}]}'
```

Sample response (order IDs and totals vary):

```json
{
  "id": 1,
  "customer_username": "customer",
  "status": "PLACED",
  "total": 179.98,
  "items": [
    {
      "product_id": 1,
      "product_name": "Wireless Barcode Scanner",
      "quantity": 2,
      "unit_price": 89.99
    }
  ]
}
```

List the customer's orders:

```bash
curl -s http://localhost:8000/api/orders \
  -H "Authorization: Bearer $CUSTOMER_TOKEN"
```

### 7.5 Run automated tests

```bash
docker compose exec api pytest -q
```

Illustrative output:

```text
........
8 passed in 1.4s
```

If test database files from a previous run cause unexpected behavior, stop the containers and inspect `backend/tests/`; tests should use the configured isolated SQLite database. If a test fails, capture the full error and compare it to the API and schema code before changing the expected behavior.

## 8. Run the local one-go smoke script

The included script starts the Compose stack, checks API health/readiness, and runs Pytest.

```bash
chmod +x scripts/local-check.sh
./scripts/local-check.sh
```

Example output (abbreviated):

```text
Waiting for API health...
{"status":"healthy","service":"retailops-api"}
{"status":"ready","database":"connected"}
........
8 passed in ...
Local build and API tests completed.
```

This is a one-time local verification, not a replacement for running each GitHub Actions stage separately.

---

# Part II — GitHub setup once

## 9. Create the GitHub repository and push the project

Create an empty GitHub repository, for example `retailops-devsecops`. Do not add a README from GitHub if you already have one locally.

From the project root:

```bash
git init
git branch -M main
git add .
git status
git commit -m "feat: initial RetailOps DevSecOps application"
git remote add origin https://github.com/YOUR_USER/retailops-devsecops.git
git push -u origin main
```

Replace `YOUR_USER` with your GitHub username or organization. If Git already exists, do not repeat `git init` or `git remote add`; inspect `git remote -v` and use the existing remote.

Sample output:

```text
[main (root-commit) abc1234] feat: initial RetailOps DevSecOps application
 43 files changed, ...
Enumerating objects: ...
Writing objects: 100% (...)
To https://github.com/YOUR_USER/retailops-devsecops.git
 * [new branch]      main -> main
```

Verify the repository contains `.github/workflows/` and all five workflow YAML files.

## 10. How to run each workflow

For manual workflows:
1. Open the GitHub repository.
2. Select **Actions**.
3. Select the named workflow.
4. Click **Run workflow**.
5. Select branch `main` unless the exercise specifies otherwise.
6. Click **Run workflow** and open the run to inspect each job and step.

Some workflows also trigger on pull requests, pushes, or version tags as described below.

---

# Part III — Lab 7.1: Quality Gate

## 11. Objective

Prove that the backend test suite and frontend production build pass before changes are considered ready.

## 12. Execute Lab 7.1

1. In GitHub, open **Actions → Lab 7.1 - Quality Gate**.
2. Click **Run workflow** on `main`.
3. Open the run.
4. Inspect the Python setup and dependency-install steps.
5. Inspect the `Run API tests` step.
6. Inspect the Node setup and `Build frontend` step.

Expected job outline:

```text
✓ Checkout repository
✓ Set up Python
✓ Install backend dependencies
✓ Run API tests
✓ Set up Node.js
✓ Build frontend
```

Sample Pytest output:

```text
........
8 passed in ...
```

Sample frontend build output (exact bundle sizes vary):

```text
vite v6.x.x building for production...
✓ ... modules transformed.
dist/index.html                   ...
dist/assets/index-....js          ...
✓ built in ...
```

## 13. Failure exercise

On a temporary branch, deliberately change a test expectation or introduce a controlled defect in a disposable copy. Commit and push it, then open the workflow run. The expected result is a red `Run API tests` or `Build frontend` step. Revert the defect and rerun.

```bash
git switch -c lab/quality-gate-failure
# Make one controlled test/code change, then:
git add .
git commit -m "test: demonstrate quality gate failure"
git push -u origin lab/quality-gate-failure
```

Create a pull request to `main` to trigger the pull-request workflow. Do not merge the deliberately failing change. After observing the failure, restore the code and delete the temporary branch.

**Evidence to capture:** workflow summary, test results, frontend build result, and a failed run from the controlled exercise.

---

# Part IV — Lab 7.2: Docker Build Gate

## 14. Objective

Verify that Docker images are built only after tests and the frontend build pass.

## 15. Execute Lab 7.2

1. Open **Actions → Lab 7.2 - Docker Build Gate**.
2. Click **Run workflow** on `main`.
3. Confirm the `test` job runs first.
4. Confirm the `build` job shows a dependency on `test`.
5. Inspect both image-build steps.

Sample output:

```text
test
  ✓ Install Python requirements
  ✓ Run Pytest
  ✓ Install frontend dependencies and build

build
  ✓ Build API image
  ✓ Build frontend image
```

Docker build logs usually include:

```text
[+] Building ...
 => [internal] load build definition from Dockerfile
 => [stage-1 ...] ...
 => exporting to image
 => naming to docker.io/library/retailops-api:lab-...
```

The exact build log and image ID vary. The images are built on the temporary GitHub-hosted runner; **Lab 7.2 does not publish them to GHCR**.

## 16. Failure exercise

Make a temporary failing test on a branch and run Lab 7.2 manually on that branch. In the supplied workflow the `build` job is limited to `main`, so a non-main branch will skip the build regardless; to demonstrate the dependency specifically, use a controlled failing test on a temporary commit in a lab-only repository/branch configuration where the build job condition permits execution. Do not push failing code into your production branch.

Expected behavior when the build job is eligible but tests fail:

```text
test: failure
build: skipped (dependency job failed)
```

---

# Part V — Lab 7.3: Checkov IaC Security Scan

## 17. Objective

Scan Terraform and Kubernetes configuration for security and configuration issues without provisioning cloud resources.

## 18. Execute Lab 7.3

1. Open **Actions → Lab 7.3 - Checkov IaC Scan**.
2. Click **Run workflow** on `main`.
3. Inspect the Checkov step.
4. Review any failed checks and the file/line information reported.

Sample output is illustrative; the supplied workflow and manifests may produce different findings depending on Checkov's version and policy database:

```text
Checkov
  Scanning ...
  Framework: terraform, kubernetes
  Passed checks: ...
  Failed checks: ...
  Skipped checks: ...
```

The workflow scans repository IaC and does not run `terraform apply`.

## 19. Learning exercise: fix a finding

1. Create a temporary branch.
2. Review a finding in a Kubernetes manifest, such as a missing security context or resource constraint.
3. Change one control at a time.
4. Commit and rerun the scan.
5. Compare the finding before and after.
6. Keep the final manifest aligned with the application requirements.

```bash
git switch -c lab/checkov-review
# Edit a manifest based on a real finding in your workflow output.
git diff
git add k8s/
git commit -m "security: remediate reviewed Kubernetes finding"
git push -u origin lab/checkov-review
```

Do not delete checks or enable soft-fail merely to obtain a green run. Explain any accepted exception and its risk.

**Evidence to capture:** Checkov summary, one reviewed finding, remediation diff, and rescan result.

---

# Part VI — Lab 7.4: Release and Environment Gates

## 20. Objective

Demonstrate separate staging and production release controls using GitHub Environments.

## 21. Configure GitHub Environments once

1. Go to repository **Settings → Environments**.
2. Create an environment named `staging`.
3. Create an environment named `production`.
4. Add required reviewers to `production` if that feature is available for the repository and plan.
5. Save the settings.

Environment names must match the workflow exactly.

## 22. Trigger staging simulation

The supplied workflow listens to pushes to `main`. Make a harmless documentation change and push it:

```bash
echo "\nStaging gate exercise." >> docs/LAB-7.1-TO-7.5.md
git add docs/LAB-7.1-TO-7.5.md
git commit -m "docs: trigger staging gate exercise"
git push origin main
```

Expected workflow log:

```text
Staging release simulation
Commit: <full Git commit SHA>
This lab stage demonstrates environment gating; it does not deploy.
```

## 23. Trigger the production gate with a version tag

After the staging simulation succeeds:

```bash
git tag v1.0.0
git push origin v1.0.0
```

Expected behavior:
- The production job starts for a tag matching `v*.*.*`.
- If required reviewers are configured, the job waits for approval.
- A reviewer can approve or reject the job.
- The job prints a production release simulation after approval.

Example log:

```text
Production approval gate passed for tag v1.0.0
Commit: <full Git commit SHA>
This lab stage demonstrates environment gating; it does not deploy.
```

If a tag already exists, choose a new version such as `v1.0.1`. The supplied workflow is a gate demonstration only; it does not publish or deploy the application.

**Evidence to capture:** staging run, production tag run, approval screen if available, and final job result.

---

# Part VII — Lab 7.5: Zero-Trust Delivery

## 24. Objective

Run tests and IaC scanning first, build both images, scan the exact images with Trivy, and publish immutable Git-SHA-tagged images only after the scans pass.

## 25. Prepare GHCR permissions

1. Open repository **Settings → Actions → General**.
2. Confirm GitHub Actions is enabled.
3. Under workflow permissions, allow the workflow to use the permissions declared in YAML.
4. The Stage 7.5 workflow requests `packages: write` only for the publishing job.
5. If your organization restricts package creation, follow its approved package policy.

The workflow uses `GITHUB_TOKEN`; do not add a personal access token to the repository unless your organization explicitly requires a different design.

## 26. Execute Lab 7.5

1. Push the reviewed code to `main`.
2. Open **Actions → Lab 7.5 - Zero Trust Delivery**.
3. Click **Run workflow** and select `main`.
4. Watch `security-gate` first.
5. Confirm API tests pass.
6. Confirm Checkov passes.
7. Inspect `build-scan-publish`.
8. Confirm the API and frontend images build with the same full Git SHA.
9. Inspect both Trivy scan steps.
10. Confirm the GHCR login and push steps run only if both scans pass.

Expected job order:

```text
security-gate
  ✓ API tests
  ✓ Checkov IaC scan

build-scan-publish
  ✓ Set lowercase image namespace
  ✓ Build API image
  ✓ Build frontend image
  ✓ Scan API image with Trivy
  ✓ Scan frontend image with Trivy
  ✓ Login to GHCR
  ✓ Publish scanned images
```

Sample image names:

```text
ghcr.io/YOUR_USER/retailops-api:<GITHUB_SHA>
ghcr.io/YOUR_USER/retailops-web:<GITHUB_SHA>
```

Replace `YOUR_USER` with the repository owner and `<GITHUB_SHA>` with the actual full commit SHA shown in the workflow. The workflow computes the lowercase owner for the registry path.

## 27. Review Trivy results

The supplied workflow fails the scan step when Trivy reports vulnerabilities at `HIGH` or `CRITICAL` severity that match the configured scan policy, excluding unfixed findings.

Example only:

```text
Total: 0 (HIGH: 0, CRITICAL: 0)
```

Another possible output:

```text
Total: 4 (HIGH: 3, CRITICAL: 1)
Process exit code: 1
```

If a scan fails:
1. Identify the affected OS package or application dependency.
2. Check for an available patched version or updated base image.
3. Rebuild the image.
4. Rerun the workflow.
5. Do not bypass the gate just to publish an image.

Actual vulnerabilities and counts depend on the base images, dependency resolution, and the date of the scan.

## 28. Verify the package in GHCR

After a successful workflow:
1. Open the repository owner’s GitHub profile/organization.
2. Open **Packages**.
3. Select `retailops-api` and `retailops-web`.
4. Verify the image versions include the commit SHA.
5. Review package visibility and access settings.

For private packages, configure Kubernetes image-pull access. Never put registry credentials in a Git-tracked manifest.

---

# Part VIII — Kubernetes Deployment Preparation

## 29. Understand what must exist before deploying

The included Kubernetes manifests are a deployment scaffold. Before they can run, you must provide:

- A Kubernetes cluster and permission to deploy into it
- API and frontend images published by Lab 7.5
- The actual GHCR owner and full Git-SHA image tags
- A PostgreSQL database reachable from the API pods
- Kubernetes Secret values for database URL, JWT secret, and demo user passwords
- A compatible ingress controller and DNS/TLS setup if public access is required

The supplied Kubernetes scaffold does **not** create PostgreSQL. It assumes an external database. For cloud environments, prefer a managed database and managed secret service.

## 30. Update the image references

Edit:
- `k8s/api-deployment.yaml`
- `k8s/web-deployment.yaml`

Replace placeholders such as:

```yaml
image: ghcr.io/YOUR_GITHUB_OWNER/retailops-api:REPLACE_WITH_GIT_SHA
```

with the exact SHA-tagged image from the successful Lab 7.5 run. Do the same for the web image. Do not use `latest` for this exercise.

## 31. Create the namespace and secrets

For a training cluster, use a terminal to create the namespace and Secret. Use your actual database endpoint and strong, unique passwords. Avoid placing secret values in shell history in shared environments; a cloud secret manager or approved secret injection mechanism is preferred.

```bash
kubectl create namespace retailops
kubectl -n retailops create secret generic retailops-secrets \
  --from-literal=DATABASE_URL='postgresql+psycopg://USER:PASSWORD@YOUR_DB_HOST:5432/retailops' \
  --from-literal=JWT_SECRET_KEY='REPLACE_WITH_RANDOM_SECRET_AT_LEAST_32_CHARS' \
  --from-literal=ADMIN_PASSWORD='REPLACE_ADMIN_PASSWORD' \
  --from-literal=WAREHOUSE_PASSWORD='REPLACE_WAREHOUSE_PASSWORD' \
  --from-literal=CUSTOMER_PASSWORD='REPLACE_CUSTOMER_PASSWORD'
```

Expected output:

```text
namespace/retailops created
secret/retailops-secrets created
```

If the namespace already exists, `kubectl create namespace` may report `AlreadyExists`; that is not necessarily an error.

## 32. Apply the manifests

From the project root:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/api-deployment.yaml
kubectl apply -f k8s/web-deployment.yaml
```

Sample output:

```text
namespace/retailops unchanged
configmap/retailops-config created
deployment.apps/retailops-api created
service/retailops-api created
deployment.apps/retailops-web created
service/retailops-web created
```

Check rollout status:

```bash
kubectl rollout status deployment/retailops-api -n retailops
kubectl rollout status deployment/retailops-web -n retailops
kubectl get pods,svc -n retailops
```

Example:

```text
NAME                                 READY   STATUS    RESTARTS
pod/retailops-api-...                2/2     Running   0
pod/retailops-web-...                2/2     Running   0
```

Exact pod names and readiness counts vary. If pods are `ImagePullBackOff`, check image names, package visibility, and image-pull credentials. If pods restart, inspect logs and events:

```bash
kubectl logs deployment/retailops-api -n retailops
kubectl describe pods -n retailops
kubectl get events -n retailops --sort-by=.lastTimestamp
```

## 33. Test services with port-forwarding

Use two terminals.

Terminal 1:

```bash
kubectl -n retailops port-forward svc/retailops-web 8080:80
```

Terminal 2:

```bash
kubectl -n retailops port-forward svc/retailops-api 8000:8000
```

Then open `http://localhost:8080` and `http://localhost:8000/health`.

The API’s CORS allow-list in this training project is configured for localhost development origins. If you serve the frontend from a different public hostname, update the API CORS configuration to match the real origin and rebuild the image.

---

# Part IX — Argo CD GitOps

## 34. Configure the Argo CD Application

1. Install Argo CD in the target cluster.
2. Ensure Argo CD can read your Git repository.
3. Edit `gitops/argocd/application.yaml`.
4. Replace the example repository URL with your actual Git URL.
5. Confirm `path: k8s` points to the manifests you intend Argo CD to manage.
6. Ensure the manifests already reference the correct image SHA and required secrets exist in the target namespace.

Apply the Application:

```bash
kubectl apply -f gitops/argocd/application.yaml
```

Example:

```text
application.argoproj.io/retailops created
```

Check application status:

```bash
kubectl -n argocd get applications
```

Example:

```text
NAME        SYNC STATUS   HEALTH STATUS
retailops   Synced        Healthy
```

Status can initially show `OutOfSync`, `Progressing`, or `Degraded` while resources are created or if configuration is incomplete.

Optional Argo CD CLI checks:

```bash
argocd app get retailops
argocd app sync retailops
```

**GitOps rule:** the pipeline publishes images, but it does not automatically commit the new image SHA to the GitOps manifests. Update the manifest through a reviewed Git commit (or add a dedicated, tightly permissioned image-update workflow) so Argo CD deploys the exact scanned artifact.

---

# Part X — Troubleshooting

## 35. Docker Compose issues

```bash
docker compose ps
docker compose logs --tail=100 db
docker compose logs --tail=100 api
docker compose logs --tail=100 web
```

Common checks:
- Docker daemon is running.
- Ports 8000 and 8080 are not already occupied.
- `.env` exists and `DATABASE_URL` points to host `db` inside Compose.
- The API can connect to PostgreSQL.
- If you change database credentials after the volume has already been initialized, PostgreSQL may retain the old initialized credentials; inspect the volume and use a deliberate reset only if disposable lab data can be lost.

To stop the local stack:

```bash
docker compose down
```

To delete the local database volume as well (destructive; deletes lab data):

```bash
docker compose down -v
```

## 36. API returns 401 or 403

- `401`: log in again and use `Authorization: Bearer <token>`.
- `403`: the authenticated role does not have permission for that endpoint.
- Confirm username/password values in `.env` match the seeded accounts.
- If you changed environment passwords after the database was already seeded, existing password hashes are not automatically updated; reset only in a disposable lab database or implement an explicit user-management/reset procedure.

## 37. GitHub Actions cannot publish GHCR images

- Verify the publishing job has `packages: write`.
- Verify GitHub Actions is enabled.
- Check organization/repository package creation policies.
- Confirm the repository owner/image namespace is correct and lowercase.
- Inspect the exact error from `docker login` or `docker push`.
- If the scan fails, publishing is intentionally not reached.

## 38. Kubernetes pods do not become Ready

```bash
kubectl get pods -n retailops
kubectl describe pods -n retailops
kubectl logs deployment/retailops-api -n retailops
kubectl get events -n retailops --sort-by=.lastTimestamp
```

Likely causes:
- Image tag does not exist or private package cannot be pulled.
- Secret name or key is missing.
- Database endpoint, credentials, networking, or TLS requirements are wrong.
- The app cannot connect to the database.
- Readiness/liveness probe is failing.

## 39. Argo CD is OutOfSync or Degraded

- Confirm repository URL, revision, and manifest path.
- Confirm Argo CD has Git repository access.
- Confirm Kubernetes image tags are the intended SHA tags.
- Confirm secrets are provisioned separately from Git.
- Review Argo CD application events and Kubernetes pod logs.
- Correct the desired state in Git and let Argo CD reconcile it.

---

# Part XI — Final Assessment

## 40. Student checklist

- [ ] Docker Compose starts PostgreSQL, FastAPI, and React/Nginx.
- [ ] `/health` and `/ready` return successful responses.
- [ ] Product catalog returns seeded products.
- [ ] JWT login returns a token for a demo account.
- [ ] Customer role cannot update inventory or view admin summary.
- [ ] Valid order reduces stock.
- [ ] Invalid or excessive order is rejected.
- [ ] Lab 7.1 quality workflow passes.
- [ ] Lab 7.2 build waits for the test job.
- [ ] Lab 7.3 Checkov findings are reviewed.
- [ ] Lab 7.4 staging/production gate behavior is observed.
- [ ] Lab 7.5 scans both images and publishes only after success.
- [ ] Kubernetes manifests use the correct image SHA and secrets are not committed.
- [ ] Kubernetes workloads become Ready.
- [ ] Argo CD reports the desired application state as Synced and Healthy.

## 41. Suggested student deliverables

Submit:
1. Screenshots of the local dashboard and API docs.
2. Test output and one intentional quality-gate failure.
3. GitHub Actions run links for all five labs.
4. One Checkov finding with remediation evidence.
5. Staging and production environment-gate evidence.
6. Trivy scan summaries and GHCR SHA-tagged package references.
7. Kubernetes rollout output and Argo CD status.
8. A short incident note explaining one failure, root cause, and corrective action.

---

## Important implementation notes

- Sample outputs are examples, not guaranteed exact output.
- This is an educational reference project, not a production-certified application.
- Do not commit `.env`, JWTs, registry credentials, or Kubernetes Secrets.
- Do not run `terraform apply`; the Terraform directory is a scanning fixture and no cloud resources are provisioned by these workflows.
- The release workflow is a simulation; the zero-trust workflow builds/scans/publishes images, and Kubernetes/Argo CD deployment is a separate configured step.
- For production use, add database migrations, transactional stock handling/locking for concurrent orders, TLS, managed secrets, backups, rate limiting, monitoring, and security review.
