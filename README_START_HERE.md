# RetailOps Progressive DevSecOps Labs 7.1–7.5

Each numbered folder is a **fully standalone project** with its own frontend, backend, database, Docker Compose, scripts, GitHub Actions workflow, step-by-step manual, and **five Mermaid diagrams** (25 diagrams total across five folders).

## Quick start in WSL2
```bash
cd 7.1
bash scripts/deploy.sh
bash scripts/test.sh
bash scripts/destroy.sh
cd ../7.2
```
Repeat with 7.3, 7.4, and 7.5. You do not need to copy code or navigate into subfolders to run commands. The `scripts/` commands are executed from the lab root.

**Important:** Each lab is independent, so it has its own `.github/workflows/`. To execute GitHub Actions, push that lab's **contents** as the root of a GitHub repository (five repos or a reused lab repo). Nested workflows in a single monorepo will not be discovered automatically by GitHub Actions.

**WSL first:** Docker Compose is the default for all five stages. Kubernetes + Argo CD is an optional advanced extension in 7.5; AWS is not required.
