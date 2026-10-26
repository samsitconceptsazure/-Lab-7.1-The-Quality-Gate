# API and test guide

Interactive API documentation: `http://localhost:8000/docs`.

## Demo identities
The seed process creates `admin`, `warehouse`, and `customer` users from environment variables. Passwords are defined in `.env.example`; use only locally and rotate them for shared environments.

## Endpoints

| Method | Path | Access | Purpose |
|---|---|---|---|
| GET | `/health` | Public | Liveness |
| GET | `/ready` | Public | Database readiness |
| POST | `/api/auth/login` | Public | Issue JWT |
| GET | `/api/auth/me` | Authenticated | Current identity and role |
| GET | `/api/products` | Public | List catalog |
| POST | `/api/products` | Admin, warehouse | Add product |
| PATCH | `/api/products/{id}/stock?stock=N` | Admin, warehouse | Set stock |
| POST | `/api/orders` | Authenticated | Place order |
| GET | `/api/orders` | Authenticated | Customer sees own orders; staff sees all |
| PATCH | `/api/orders/{id}/status?status_value=SHIPPED` | Admin, warehouse | Fulfillment workflow |
| GET | `/api/admin/summary` | Admin | Operational summary |

## API smoke test

```bash
TOKEN=$(curl -s http://localhost:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"customer","password":"ChangeMe_Customer_123!"}' | python -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')

curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/auth/me
curl http://localhost:8000/api/products
```

Place an order using a real product ID:
```bash
curl -X POST http://localhost:8000/api/orders \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d '{"items":[{"product_id":1,"quantity":1}]}'
```

## Tests
Run with Docker Compose:
```bash
docker compose exec api pytest -q
```
Or locally:
```bash
cd backend
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

The tests exercise health/readiness, login failure, seeded catalog, order creation and stock decrement, role denial, authentication enforcement, stock validation, and admin-only reporting.
