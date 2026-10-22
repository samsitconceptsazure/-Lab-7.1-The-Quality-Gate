# RetailOps DevSecOps Lab — 20 Infographic Blueprints

**Project:** RetailOps Enterprise Order Management  
**Stack:** React, FastAPI, PostgreSQL, JWT/RBAC, Docker, GitHub Actions, Checkov, Trivy, GHCR, Kubernetes, Argo CD  
**Purpose:** Teaching and presentation pack for Labs 7.1–7.5.

> This Markdown file contains 20 ready-to-design infographic briefs. Each brief includes a title, key visual layout, core content, and suggested visual treatment. They can be used as image-generation prompts or as specifications for a designer. The diagrams describe the lab architecture and workflow; they are not screenshots of a running deployment.

## Shared visual style

- **Format:** 16:9 landscape for slides; adapt to portrait for posters.
- **Look:** polished enterprise technology infographic, clean vector illustrations, crisp labels, high contrast, readable text, consistent iconography.
- **Palette:** navy blue and white base, with cyan for application flow, green for successful gates, amber for build/release, violet for GitOps, and red for blocked security gates.
- **Branding:** “RetailOps — DevSecOps Zero Trust Labs 7.1–7.5”.
- **Design rule:** use arrows for flow, numbered stages for sequence, and concise labels. Avoid fake metrics, invented deployment results, or unreadably tiny text.

---

## Infographic 01 — RetailOps at a Glance

**Purpose:** Introduce the business application before discussing its pipeline.

**Visual layout:** Center a browser-style RetailOps dashboard. Surround it with five feature callouts: Product Catalog, Order Management, Inventory Control, Role-Based Access, and Operational Dashboard.

**Content to show:**
- Users browse products and stock levels.
- Authenticated users place orders.
- Orders reduce inventory.
- Warehouse/admin roles manage fulfillment.
- Customers can see their own orders; staff access is broader according to role.

**Bottom technology strip:** React UI → FastAPI REST API → PostgreSQL.

**Image brief:** Create a polished enterprise software infographic showing a fictional RetailOps order-management dashboard and its core business capabilities, with a navy header, white canvas, cyan/green accents, simple vector icons, and readable callouts. Keep the product interface illustrative rather than claiming it is a real screenshot.

---

## Infographic 02 — End-to-End System Architecture

**Purpose:** Explain how the application components communicate.

**Visual layout:** Three horizontal tiers:
1. **Presentation:** React application served by NGINX.
2. **Application:** FastAPI endpoints, JWT validation, business rules, order/inventory logic.
3. **Data:** PostgreSQL users, products, orders, and order items.

Add a side rail for GitHub Actions, GHCR, Kubernetes, and Argo CD, showing delivery rather than runtime traffic.

**Content to show:** Browser requests go to the API; the API reads/writes PostgreSQL; CI builds images; GitOps deploys approved manifests.

**Image brief:** Design a clear three-tier architecture infographic for RetailOps with React/NGINX, FastAPI, and PostgreSQL stacked vertically, request arrows between tiers, and a separate CI/CD delivery rail. Use accurate labels and distinguish runtime traffic from deployment flow.

---

## Infographic 03 — The Five-Lab Learning Journey

**Purpose:** Show the learning progression across Labs 7.1–7.5.

**Visual layout:** Five connected numbered cards:
1. **7.1 Quality Gate** — Pytest and frontend build.
2. **7.2 Docker Build Gate** — build only after tests pass.
3. **7.3 Security Sentinel** — Checkov scans Terraform/Kubernetes configuration.
4. **7.4 Release Manager** — staging and production environment gates.
5. **7.5 Zero-Trust Delivery** — tests, IaC scan, image build, Trivy scan, GHCR publish.

**Footer:** “One application. One repository. Five progressive controls.”

**Image brief:** Create a horizontal five-stage DevSecOps learning-roadmap infographic for RetailOps. Use distinct blue, amber, red/pink, violet, and green stage panels, numbered circles, short descriptions, and directional arrows.

---

## Infographic 04 — Lab 7.1: Quality Gate

**Purpose:** Teach why tests and builds run before packaging.

**Visual layout:** Source change enters a gate; two parallel checks run:
- Backend: install requirements → Pytest API tests.
- Frontend: install packages → production build.

Both checks must pass to produce a green “Quality approved” result. A red branch shows a failing test blocking the workflow.

**Examples of tests:** login failure, role denial, order placement, stock decrement, insufficient stock, health/readiness.

**Image brief:** Create a CI quality-gate infographic with code entering a two-lane test pipeline for FastAPI/Pytest and React/Vite build. Show pass/fail branches and make the blocked-on-failure behavior visually obvious.

---

## Infographic 05 — Lab 7.2: Docker Build Gate

**Purpose:** Explain dependency ordering between tests and container builds.

**Visual layout:** `Checkout → Test job → Build job → API image + Web image`.

Draw a hard dependency arrow from Test to Build. If tests fail, show the build job as skipped, not successful.

**Images built:**
- FastAPI API container.
- React frontend served by NGINX.

**Important note:** This stage builds images for validation; it does not publish them to a registry.

**Image brief:** Design a Docker build-gate infographic with a visible job dependency, two resulting container images, and a red stop sign showing that a failed test prevents image builds. Include “Build only after tests pass.”

---

## Infographic 06 — Lab 7.3: Infrastructure-as-Code Security

**Purpose:** Teach policy scanning before infrastructure deployment.

**Visual layout:** Terraform and Kubernetes YAML enter Checkov. Results flow to:
- compliant configuration → review/continue;
- policy findings → fix and scan again.

**Content to show:** Checkov examines configuration and security posture; the lab workflow does not run `terraform apply` or provision cloud resources.

**Image brief:** Create an IaC security infographic with Terraform files and Kubernetes manifests flowing into a Checkov scanner, producing a findings report and a remediation loop. Add a clear “Scan only — no infrastructure deployment” note.

---

## Infographic 07 — Lab 7.4: Staging and Production Release Gates

**Purpose:** Explain release promotion and approvals.

**Visual layout:** `Push to main → Staging environment` and separately `Version tag vX.Y.Z → Production environment → reviewer approval gate`.

Show the production path paused until approval. Mark this lab stage as a release-gate simulation.

**Content to show:** GitHub Environments can hold protection rules and secrets; required reviewer availability depends on repository settings and plan.

**Image brief:** Design a release-management infographic with a staging lane and a protected production lane, version-tag marker, reviewer approval checkpoint, and a visible pause-until-approved symbol. Clearly label the included workflow as a simulation, not an actual deployment.

---

## Infographic 08 — Lab 7.5: Zero-Trust Delivery Pipeline

**Purpose:** Present the final security chain from source to published images.

**Visual layout:** Five sequential gates:
1. Pytest and frontend build.
2. Checkov IaC scan.
3. Build API and web images.
4. Trivy scans both images.
5. Publish images to GHCR using the Git commit SHA.

Any failed gate stops the path. Image publishing occurs only after both image scans pass.

**Image brief:** Create a detailed but readable zero-trust CI/CD pipeline infographic for RetailOps, with green check gates, red failure exits, Docker image symbols, Trivy magnifier/shield, and GHCR registry. Emphasize “scan before publish” and immutable Git-SHA tags.

---

## Infographic 09 — GitHub Actions Workflow Relationships

**Purpose:** Clarify the role of each workflow and avoid assuming all workflows run together.

**Visual layout:** Five separate workflow cards, each with its trigger:
- 7.1: manual dispatch and pull requests to main.
- 7.2: manual dispatch.
- 7.3: manual dispatch and relevant IaC pull-request changes.
- 7.4: pushes to main, version tags, and manual dispatch.
- 7.5: manual dispatch.

Use dotted connectors to show they share the same repository, not a single automatic chain.

**Image brief:** Create a workflow-map infographic with five distinct GitHub Actions workflow cards and their triggers. Show that Labs 7.1–7.5 are independently testable workflows sharing one repository, not necessarily one automatically chained workflow.

---

## Infographic 10 — JWT Authentication: Login to API

**Purpose:** Explain how a user obtains and uses a token.

**Visual layout:** User submits username/password → FastAPI verifies credentials → signed JWT returned → browser sends bearer token → protected API validates token → response returned.

Show an invalid credential/token path ending in a 401 response.

**Security notes:** Keep the JWT signing secret out of source control; use HTTPS and strong secrets outside localhost training.

**Image brief:** Design a sequence infographic for JWT authentication in RetailOps with a browser, login endpoint, signed token, Authorization Bearer header, protected API, and 401 failure path. Do not depict a JWT as encrypted user data; label it as a signed access token.

---

## Infographic 11 — Role-Based Access Control

**Purpose:** Explain the application’s three roles and their access boundaries.

**Visual layout:** Three role cards:
- **Customer:** view catalog, place orders, view own orders.
- **Warehouse:** manage stock and order fulfillment; view staff-visible orders.
- **Admin:** warehouse permissions plus administrative summary.

At the bottom, show an API authorization check before protected actions.

**Image brief:** Create a role-based access control infographic with customer, warehouse, and admin lanes. Use a permission matrix and a central API authorization gate. Highlight least privilege and show a customer request to an admin endpoint being denied.

---

## Infographic 12 — Order Lifecycle and Inventory Integrity

**Purpose:** Explain the main business transaction.

**Visual layout:** Select product → validate requested quantity → verify stock → create order → decrement stock → warehouse updates status → shipment/delivery.

Add a red branch for insufficient stock and a cancellation branch that restores stock in the sample implementation.

**Image brief:** Create a retail order lifecycle infographic showing stock validation before order creation, inventory decrement on successful order, status progression through fulfillment, and stock restoration on cancellation. Include a clear insufficient-stock rejection path.

---

## Infographic 13 — PostgreSQL Data Model

**Purpose:** Introduce the core persisted entities.

**Visual layout:** Four entity cards and relationships:
- `users`: username, password hash, role.
- `products`: SKU, name, description, price, stock.
- `orders`: customer username, status, total, created timestamp.
- `order_items`: order ID, product ID, product name, quantity, unit price.

Show one order having multiple order items and each item referencing a product.

**Image brief:** Design a simple database relationship infographic for RetailOps with four table cards, field names, and clear relationship arrows. Avoid inventing fields or implying a full enterprise data warehouse.

---

## Infographic 14 — Docker Compose Local Environment

**Purpose:** Help students understand the local runnable environment.

**Visual layout:** One Docker Compose boundary containing:
- PostgreSQL container with persistent named volume.
- FastAPI API container on port 8000.
- React/NGINX web container on port 8080.

Show the API waiting for database health and the browser accessing the web UI.

**Image brief:** Create a Docker Compose topology infographic with three containers, ports, the PostgreSQL volume, and service dependency arrows. Clearly label the local URLs and distinguish persistent database storage from ephemeral containers.

---

## Infographic 15 — Container Image Security with Trivy

**Purpose:** Explain image scanning and the publication gate.

**Visual layout:** API image and web image → Trivy vulnerability scanner → severity policy gate → GHCR.

A HIGH/CRITICAL finding under the configured workflow policy stops publishing. A passing scan allows the exact SHA-tagged image to be pushed.

**Content note:** Findings depend on current package versions and scanner databases; do not show invented CVE counts.

**Image brief:** Create a container-security infographic showing two image scans, Trivy vulnerability analysis, a policy decision, and GHCR publication only on pass. Do not invent vulnerability totals or claim every vulnerability can always be fixed.

---

## Infographic 16 — Immutable Image Tags and Provenance

**Purpose:** Explain why the commit SHA is used as the image tag.

**Visual layout:** Git commit SHA → build → scan → image tagged with the same SHA → GHCR → Kubernetes manifest references that tag.

Contrast a mutable `latest` tag with an immutable commit-specific tag, without claiming that a tag alone proves cryptographic provenance.

**Image brief:** Design an artifact traceability infographic connecting a source commit, scanned container image, GHCR tag, and Kubernetes deployment. Emphasize exact SHA matching and distinguish traceability from a full signed-attestation system.

---

## Infographic 17 — Kubernetes Runtime Architecture

**Purpose:** Explain how the app runs after deployment.

**Visual layout:** Namespace `retailops` containing:
- Two API replicas and API Service.
- Two web replicas and web Service.
- ConfigMap for non-secret settings.
- Secret references for database URL, JWT secret, and demo passwords.
- Readiness/liveness probes and resource requests/limits.

Show PostgreSQL as an external managed database for the cloud-ready variant.

**Image brief:** Create a Kubernetes runtime architecture infographic for RetailOps showing two web replicas, two API replicas, Services, ConfigMap, Secret references, health probes, and an external PostgreSQL database. Make it clear that database provisioning is outside the supplied manifests.

---

## Infographic 18 — Kubernetes Security Controls

**Purpose:** Highlight the hardening choices in the sample manifests.

**Visual layout:** Pod security checklist:
- Non-root user.
- `allowPrivilegeEscalation: false`.
- Drop Linux capabilities.
- RuntimeDefault seccomp profile.
- Read-only root filesystem where configured.
- Resource requests and limits.
- Service-account token automount disabled.
- Secrets referenced rather than stored in manifest files.

**Image brief:** Create a Kubernetes workload-hardening infographic using a pod cutaway and a concise checklist of controls from the supplied manifests. Add a note that these controls reduce risk but do not alone make an application production-secure.

---

## Infographic 19 — Argo CD GitOps Reconciliation

**Purpose:** Explain declarative delivery and desired-state reconciliation.

**Visual layout:** Git repository `k8s/` manifests → Argo CD detects changes → compares desired and live state → syncs changes → Kubernetes workloads → health/sync status returned.

Show self-healing as correction of drift toward the committed desired state. Add a caution that automatic sync/prune can remove resources if manifests are wrong.

**Image brief:** Create a GitOps infographic with Git as the desired-state source, Argo CD reconciliation loop, Kubernetes cluster, and sync/health indicators. Show that image tags must be updated in Git before Argo CD can deploy a new SHA-tagged image.

---

## Infographic 20 — Full Lab Validation and Troubleshooting Map

**Purpose:** Provide students with a final checklist and a first-response troubleshooting guide.

**Visual layout:** Left side: validation checklist. Right side: symptom-to-check map.

**Validation checklist:**
- UI responds on port 8080.
- API docs respond on port 8000/docs.
- `/health` and `/ready` respond.
- Customer login works and cannot access admin-only endpoints.
- Orders decrement inventory; over-ordering is rejected.
- Labs 7.1–7.5 have been run and evidence captured.
- Images have passed Trivy before publishing.
- Kubernetes uses exact SHA image tags and external secrets.
- Argo CD reports expected sync/health state.

**Troubleshooting map:**
- UI unavailable → inspect web container logs and port mapping.
- API unavailable → inspect API logs and `/health`.
- Database readiness fails → inspect database health, URL, credentials, and networking.
- 401 → check login credentials/token expiry/header.
- 403 → check role permissions.
- CI test failure → inspect failing assertion before changing the pipeline.
- Trivy blocks publish → review findings and update base image/dependencies.
- Pod `ImagePullBackOff` → verify image name/tag, registry visibility, and pull credentials.
- Argo CD out of sync → inspect repository URL/path, manifest validity, and image tags.

**Image brief:** Create a final lab operations infographic with a completion checklist and symptom-to-first-check troubleshooting map. Use green checks for validated items, amber warnings for configuration issues, and red for blocked pipeline gates. Do not imply that unexecuted checks have passed.

---

## Suggested teaching order

1. Infographics 01–03: business context, architecture, learning journey.
2. Infographics 04–09: pipeline controls and workflow triggers.
3. Infographics 10–13: application security, business flow, and data model.
4. Infographics 14–19: local containers, image security, Kubernetes, and GitOps.
5. Infographic 20: final validation and troubleshooting.

## Accuracy notes for instructors

- The included Lab 7.4 workflow is an environment/release-gate **simulation**; it does not deploy the app.
- Lab 7.3 scans IaC; it does not provision infrastructure.
- Lab 7.5 builds and scans both images, then publishes them with the commit SHA only if the configured gates pass.
- The supplied Kubernetes manifests require environment-specific image tags, a reachable PostgreSQL database, and a Kubernetes Secret created outside Git.
- The sample is a training foundation, not a claim of production certification. Add TLS, external secret management, migrations, backups, rate limiting, monitoring, and deployment-specific review before production use.
