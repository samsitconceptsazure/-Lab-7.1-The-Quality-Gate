# Instructor guide: Labs 7.1–7.5 using RetailOps

## Lab 7.1 — Quality gate
**Goal:** stop low-quality changes before packaging.
- Run workflow `Lab 7.1 - Quality Gate`.
- Inspect API tests and frontend build.
- Exercise: break the stock validation or change a response contract; confirm the workflow fails; restore the change.
- Evidence: passing tests, frontend build output, failed run from a controlled defect.

## Lab 7.2 — Docker build gate
**Goal:** build only after tests pass.
- Run workflow `Lab 7.2 - Docker Build Gate` on `main`.
- Verify the `build` job depends on `test`.
- Exercise: introduce a failing test and confirm the build job is skipped.
- Images are built but not pushed.

## Lab 7.3 — Infrastructure-as-code security
**Goal:** scan IaC before deployment.
- Run workflow `Lab 7.3 - Checkov IaC Scan`.
- Inspect Terraform and Kubernetes findings; severity and policy results may vary as Checkov rules evolve.
- Exercise: create a temporary branch, remove a Kubernetes security control, scan and compare; restore the manifest.
- This workflow never applies Terraform.

## Lab 7.4 — Environment-based release control
**Goal:** model staging and production gates.
- Configure GitHub Environments `staging` and `production`.
- Add required reviewers to `production` if available in your repository/plan.
- Push to `main` for the staging simulation.
- Tag a release: `git tag v1.0.0 && git push origin v1.0.0`.
- This stage demonstrates environment approvals; it does not deploy.

## Lab 7.5 — Zero Trust delivery
**Goal:** test, scan IaC, build, scan image, then publish immutable artifacts.
- Run workflow `Lab 7.5 - Zero Trust Delivery` on `main`.
- Verify that tests and Checkov pass before image building.
- Verify both API and web images are scanned by Trivy.
- Publishing occurs only after both scans pass and uses the Git commit SHA as the tag.
- Exercise: create a temporary image with a known vulnerable dependency in a throwaway branch and observe the Trivy gate; do not add a known vulnerable dependency to the main branch.

## Completion checklist
- [ ] Local app opens at port 8080
- [ ] API docs open at port 8000/docs
- [ ] JWT login works for each role
- [ ] Customer cannot update inventory or see admin summary
- [ ] Orders decrement stock and reject over-ordering
- [ ] Lab 7.1 quality gate passes
- [ ] Lab 7.2 build gate passes after tests
- [ ] Lab 7.3 Checkov scan is reviewed
- [ ] Lab 7.4 environment approval behavior is observed
- [ ] Lab 7.5 Trivy gates publication of SHA-tagged images
- [ ] Kubernetes manifests use exact SHA tags and secrets are not committed
- [ ] Argo CD reports the application synced and healthy
