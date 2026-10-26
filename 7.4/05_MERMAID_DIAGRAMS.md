# Lab 7.4 — Five Mermaid Diagrams

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

## 2. Lab 7.4 Environment-Based Release Gate

```mermaid
flowchart TD
    Push[Push to main] --> Staging[GitHub staging environment]
    Staging --> StageSim[Staging release simulation]
    Tag[Push version tag vX.Y.Z] --> Production[GitHub production environment]
    Production --> Approval{Required reviewer approval configured?}
    Approval -- Yes --> Wait[Wait for reviewer decision]
    Wait --> Decision{Approved?}
    Decision -- No --> Block[Production job blocked]
    Decision -- Yes --> ProdSim[Production release simulation]
    Approval -- No --> ProdSim
    StageSim --> Evidence[Capture workflow evidence]
    ProdSim --> Evidence
    Reminder[This lab demonstrates gates; it does not deploy the app] -.-> ProdSim
```

## 3. Database Entity Relationship

```mermaid
erDiagram
    USERS {
      int id PK
      string username UK
      string password_hash
      string role
    }
    PRODUCTS {
      int id PK
      string sku UK
      string name
      string description
      float price
      int stock
    }
    ORDERS {
      int id PK
      string customer_username
      string status
      float total
      datetime created_at
    }
    ORDER_ITEMS {
      int id PK
      int order_id FK
      int product_id FK
      string product_name
      int quantity
      float unit_price
    }
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : referenced_by
```

## 4. Argo CD GitOps Reconciliation

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

## 5. End-to-End Student Validation Checklist

```mermaid
flowchart TD
    Start([Start lab]) --> Local[Start app with Docker Compose]
    Local --> UI{UI and API available?}
    UI -- No --> FixLocal[Inspect compose logs and health]
    FixLocal --> Local
    UI -- Yes --> Auth[Test login and JWT]
    Auth --> RBAC[Test customer and staff permissions]
    RBAC --> Orders[Test order creation and stock decrement]
    Orders --> Tests[Run Pytest and frontend build]
    Tests --> S71[Run Lab 7.1]
    S71 --> S72[Run Lab 7.2]
    S72 --> S73[Run Lab 7.3]
    S73 --> S74[Run Lab 7.4]
    S74 --> S75[Run Lab 7.5]
    S75 --> Publish{Images published after scans?}
    Publish -- No --> Diagnose[Review failed gate and remediate]
    Diagnose --> S75
    Publish -- Yes --> K8s[Configure secrets and SHA image tags]
    K8s --> Argo[Sync with Argo CD]
    Argo --> Healthy{Synced and healthy?}
    Healthy -- No --> Debug[Inspect events, logs, and readiness]
    Debug --> K8s
    Healthy -- Yes --> Done([Lab complete])
```

