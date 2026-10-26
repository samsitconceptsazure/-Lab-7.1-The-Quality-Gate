# Lab 7.1 — Five Mermaid Diagrams

All diagrams are self-contained teaching visuals for this stage. Some show the complete platform context.

## 1. End-to-End RetailOps Architecture

```mermaid
flowchart TD
    User[Retail Operations User] --> UI[React Web UI]
    UI --> API[FastAPI REST API]
    API --> Auth[JWT Authentication and RBAC]
    API --> DB[(PostgreSQL)]
    API --> Catalog[Product Catalog]
    API --> Orders[Order Management]
    Orders --> Inventory[Inventory Validation]
    Inventory --> DB
    API --> Health[Health and Readiness Endpoints]
    subgraph Delivery[DevSecOps Delivery]
      GH[GitHub Repository] --> Actions[GitHub Actions]
      Actions --> Scan[Checkov and Trivy]
      Scan --> GHCR[GitHub Container Registry]
      GHCR --> K8s[Kubernetes]
      GitOps[Argo CD] --> K8s
      GH --> GitOps
    end
```

## 2. RetailOps Application Components

```mermaid
flowchart LR
    subgraph Frontend
      React[React + Vite]
      Dashboard[Operations Dashboard]
      CatalogUI[Product Catalog UI]
      OrdersUI[Orders UI]
      Login[Login Form]
    end
    subgraph Backend
      FastAPI[FastAPI]
      Auth[JWT Login and Identity]
      RBAC[Role Checks]
      ProductAPI[Product API]
      OrderAPI[Order API]
      AdminAPI[Admin Summary API]
    end
    subgraph Data
      PostgreSQL[(PostgreSQL)]
      Users[(Users)]
      Products[(Products)]
      OrderRows[(Orders and Order Items)]
    end
    React --> Dashboard
    React --> CatalogUI
    React --> OrdersUI
    React --> Login
    React --> FastAPI
    FastAPI --> Auth
    FastAPI --> RBAC
    FastAPI --> ProductAPI
    FastAPI --> OrderAPI
    FastAPI --> AdminAPI
    Auth --> Users
    ProductAPI --> Products
    OrderAPI --> Products
    OrderAPI --> OrderRows
    AdminAPI --> PostgreSQL
```

## 3. JWT Authentication Sequence

```mermaid
sequenceDiagram
    actor User
    participant UI as React UI
    participant API as FastAPI
    participant DB as PostgreSQL
    User->>UI: Enter username and password
    UI->>API: POST /api/auth/login
    API->>DB: Find user by username
    DB-->>API: Password hash and role
    API->>API: Verify password hash
    alt Credentials valid
      API-->>UI: Signed JWT and role
      UI->>API: Request with Bearer token
      API->>API: Verify signature and expiry
      API->>DB: Load current user
      DB-->>API: User and role
      API-->>UI: Authorized response
    else Credentials invalid
      API-->>UI: 401 Unauthorized
    end
```

## 4. Role-Based Access Control

```mermaid
flowchart TD
    Request[Incoming API request] --> Token{Bearer JWT present?}
    Token -- No --> U401[401 Unauthorized]
    Token -- Yes --> Verify{Signature and expiry valid?}
    Verify -- No --> U401
    Verify -- Yes --> Role[Load current user role]
    Role --> Endpoint{Endpoint permission}
    Endpoint -- Public catalog --> Catalog[Return products]
    Endpoint -- Customer order --> Customer{Authenticated user?}
    Customer -- Yes --> OwnOrder[Create order or list own orders]
    Endpoint -- Stock update --> Staff{Admin or warehouse?}
    Staff -- Yes --> Stock[Update inventory]
    Staff -- No --> F403[403 Forbidden]
    Endpoint -- Admin summary --> Admin{Admin?}
    Admin -- Yes --> Summary[Return admin summary]
    Admin -- No --> F403
```

## 5. Database Entity Relationship

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

