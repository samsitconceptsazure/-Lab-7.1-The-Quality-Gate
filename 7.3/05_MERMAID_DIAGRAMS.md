# Lab 7.3 — Five Mermaid Diagrams

All diagrams are self-contained teaching visuals for this stage. Some show the complete platform context.

## 1. Five-Stage Lab Roadmap

```mermaid
flowchart LR
    S71["7.1 Quality Gate<br/>Pytest + React build"] --> S72["7.2 Docker Build Gate<br/>Build after tests"]
    S72 --> S73["7.3 IaC Security<br/>Checkov"]
    S73 --> S74["7.4 Release Gate<br/>Staging + production approval"]
    S74 --> S75["7.5 Zero-Trust Delivery<br/>Tests + Checkov + Trivy + GHCR"]
    S75 --> Deploy["Kubernetes deployment"]
    Deploy --> GitOps["Argo CD reconciliation"]
```

## 2. Lab 7.3 Infrastructure-as-Code Scan

```mermaid
flowchart LR
    Repo[GitHub checkout] --> TF[terraform/]
    Repo --> K8S[k8s/ manifests]
    TF --> Checkov[Checkov scan]
    K8S --> Checkov
    Checkov --> Findings{Policy findings?}
    Findings -- Yes --> Review[Review and remediate findings]
    Findings -- No --> Pass[Scan passes]
    Review --> Commit[Commit corrected IaC]
    Commit --> Checkov
    Pass --> Next[Continue delivery workflow]
    Note[No terraform apply in this lab] -.-> TF
```

## 3. Container Image Supply Chain

```mermaid
flowchart LR
    Source[Reviewed source commit] --> DockerAPI[Build API Dockerfile]
    Source --> DockerWeb[Build web Dockerfile]
    DockerAPI --> APIImage[API image : Git SHA]
    DockerWeb --> WebImage[Web image : Git SHA]
    APIImage --> TrivyAPI[Trivy OS and library scan]
    WebImage --> TrivyWeb[Trivy OS and library scan]
    TrivyAPI --> Policy{Both scans pass policy?}
    TrivyWeb --> Policy
    Policy -- No --> Reject[Do not publish]
    Policy -- Yes --> GHCR[Push to GHCR]
    GHCR --> Digest[Registry digest and Git SHA]
    Digest --> Deploy[Use exact tag/digest in Kubernetes]
```

## 4. Kubernetes Runtime Architecture

```mermaid
flowchart TD
    Client[Browser / client] --> Ingress[Ingress controller with TLS]
    Ingress --> WebSvc[retailops-web Service]
    Ingress --> APISvc[retailops-api Service]
    WebSvc --> Web1[Web pod 1]
    WebSvc --> Web2[Web pod 2]
    APISvc --> API1[API pod 1]
    APISvc --> API2[API pod 2]
    API1 --> PG[(External PostgreSQL)]
    API2 --> PG
    API1 --> Secret[Kubernetes Secret references]
    API2 --> Secret
    Config[ConfigMap] --> API1
    Config --> API2
    Probe[Readiness and liveness probes] -. monitors .-> API1
    Probe -. monitors .-> API2
```

## 5. Observability and Troubleshooting Path

```mermaid
flowchart TD
    Symptom[User reports app issue] --> UI[Check browser and frontend]
    UI --> APIHealth[Check /health and /ready]
    APIHealth --> Pods[Check Kubernetes pods and events]
    Pods --> Logs[Inspect API and web logs]
    Logs --> DB[Verify PostgreSQL connectivity]
    DB --> Auth[Check JWT, role, and request payload]
    Auth --> Pipeline[Inspect GitHub Actions run]
    Pipeline --> Checkov[Review Checkov findings]
    Checkov --> Trivy[Review Trivy findings]
    Trivy --> GitOps[Check Argo CD sync and health]
    GitOps --> RootCause[Record root cause and remediation]
```

