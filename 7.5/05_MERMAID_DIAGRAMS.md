# Lab 7.5 — Five Mermaid Diagrams

All diagrams are self-contained teaching visuals for this stage. Some show the complete platform context.

## 1. Developer-to-Production Flow

```mermaid
flowchart TD
    Dev[Developer changes code] --> PR[Pull request or commit]
    PR --> Repo[GitHub repository]
    Repo --> CI[GitHub Actions workflow]
    CI --> Quality{Tests and build pass?}
    Quality -- No --> Fix[Review logs and fix code]
    Fix --> Dev
    Quality -- Yes --> IaC[Checkov IaC scan]
    IaC --> Sec{Security gates pass?}
    Sec -- No --> Remediate[Remediate findings]
    Remediate --> Dev
    Sec -- Yes --> Build[Build container images]
    Build --> Trivy[Trivy scan]
    Trivy --> Vuln{High/Critical findings?}
    Vuln -- Yes --> RemediateImage[Fix dependencies or base image]
    RemediateImage --> Dev
    Vuln -- No --> Publish[Publish Git-SHA images to GHCR]
    Publish --> GitOps[Update GitOps manifests with SHA]
    GitOps --> Argo[Argo CD sync]
    Argo --> K8s[Kubernetes]
```

## 2. Lab 7.5 Zero-Trust Delivery Pipeline

```mermaid
flowchart TD
    Dispatch[Manual workflow dispatch on main] --> Gate[Security gate job]
    Gate --> Tests[Pytest API tests]
    Tests --> Checkov[Checkov Terraform and Kubernetes scan]
    Checkov --> GatePass{Security gate passed?}
    GatePass -- No --> Stop[Stop; no images published]
    GatePass -- Yes --> APIBuild[Build API image tagged with Git SHA]
    APIBuild --> WebBuild[Build web image tagged with Git SHA]
    WebBuild --> ScanAPI[Trivy scan API image]
    ScanAPI --> ScanWeb[Trivy scan web image]
    ScanWeb --> Clean{Both scans pass?}
    Clean -- No --> Stop
    Clean -- Yes --> Login[Authenticate to GHCR]
    Login --> Push[Push both SHA-tagged images]
    Push --> Complete[Immutable artifact identity recorded]
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

## 5. Argo CD GitOps Reconciliation

```mermaid
flowchart TD
    Dev[Developer or release automation] --> Change[Commit manifest with approved image SHA]
    Change --> Git[GitOps source repository]
    Argo[Argo CD controller] --> Compare[Compare Git desired state with cluster]
    Git --> Compare
    Compare --> Drift{Drift or new revision?}
    Drift -- No --> Healthy[Application remains Synced]
    Drift -- Yes --> Sync[Apply desired Kubernetes manifests]
    Sync --> K8s[Kubernetes API]
    K8s --> Pods[Roll out RetailOps pods]
    Pods --> Health{Workloads healthy?}
    Health -- Yes --> Synced[Synced and Healthy]
    Health -- No --> Diagnose[Inspect events, logs, probes]
    Diagnose --> Fix[Commit corrective change]
    Fix --> Git
```

