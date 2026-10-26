# Lab 7.2 — Five Mermaid Diagrams

All diagrams are self-contained teaching visuals for this stage. Some show the complete platform context.

## 1. Lab 7.1 Quality Gate

```mermaid
flowchart TD
    Start[Workflow starts] --> Checkout[Checkout repository]
    Checkout --> PySetup[Set up Python]
    PySetup --> InstallPy[Install backend requirements]
    InstallPy --> Pytest[Run Pytest API suite]
    Pytest --> PyPass{Tests pass?}
    PyPass -- No --> Fail[Fail workflow]
    PyPass -- Yes --> Node[Set up Node.js]
    Node --> Npm[npm install]
    Npm --> Build[npm run build]
    Build --> BuildPass{Frontend build passes?}
    BuildPass -- No --> Fail
    BuildPass -- Yes --> Green[Quality gate passed]
```

## 2. Lab 7.2 Docker Build Gate

```mermaid
flowchart TD
    Trigger[Manual workflow dispatch] --> TestJob[Test job]
    TestJob --> API[Install Python requirements]
    API --> Pytest[Run Pytest]
    Pytest --> Frontend[Install frontend dependencies]
    Frontend --> NpmBuild[Build React frontend]
    NpmBuild --> TestsOK{All tests and build pass?}
    TestsOK -- No --> Skip[Build job skipped]
    TestsOK -- Yes --> Main{Ref is main?}
    Main -- No --> Skip
    Main -- Yes --> APIImage[Build FastAPI image]
    APIImage --> WebImage[Build React/Nginx image]
    WebImage --> Done[Images built locally on runner]
    Done --> Note[No image publishing in Lab 7.2]
```

## 3. Order Placement and Inventory Update

```mermaid
sequenceDiagram
    actor Customer
    participant API as FastAPI
    participant DB as PostgreSQL
    Customer->>API: POST /api/orders with product IDs and quantities
    API->>API: Validate JWT and request schema
    API->>DB: Load requested products
    DB-->>API: Price and stock per product
    API->>API: Check products exist and stock is sufficient
    alt Invalid product or insufficient stock
      API-->>Customer: 404 or 409 error
    else Valid order
      API->>DB: Decrement stock and insert order/items
      DB-->>API: Commit
      API-->>Customer: 201 Created with order summary
    end
```

## 4. Order Status Lifecycle

```mermaid
stateDiagram-v2
    [*] --> PLACED
    PLACED --> PROCESSING
    PLACED --> CANCELLED
    PROCESSING --> SHIPPED
    PROCESSING --> CANCELLED
    SHIPPED --> DELIVERED
    SHIPPED --> CANCELLED
    DELIVERED --> [*]
    CANCELLED --> [*]
    note right of DELIVERED
      Terminal state
    end note
    note right of CANCELLED
      Terminal state; app restores stock
    end note
```

## 5. Docker Compose Local Runtime

```mermaid
flowchart TD
    Browser[Browser :8080] --> Web[Nginx serving React build]
    Web --> API[FastAPI container :8000]
    API --> DB[(PostgreSQL container :5432)]
    Compose[Docker Compose] -. manages .-> Web
    Compose -. manages .-> API
    Compose -. manages .-> DB
    DB --> Volume[(Persistent named volume)]
    API --> Health[/health and /ready/]
```

