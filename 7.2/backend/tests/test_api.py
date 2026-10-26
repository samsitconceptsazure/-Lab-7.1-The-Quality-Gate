def token(client, username="admin", password="ChangeMe_Admin_123!"):
    response = client.post("/api/auth/login", json={"username": username, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]

def auth(value):
    return {"Authorization": f"Bearer {value}"}

def test_health_and_ready(client):
    assert client.get("/health").json()["status"] == "healthy"
    assert client.get("/ready").status_code == 200

def test_login_rejects_bad_password(client):
    response = client.post("/api/auth/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401

def test_seeded_catalog(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert len(response.json()) >= 5

def test_customer_can_place_order_and_stock_decreases(client):
    customer_token = token(client, "customer", "ChangeMe_Customer_123!")
    product = client.get("/api/products").json()[0]
    before = product["stock"]
    response = client.post("/api/orders", headers=auth(customer_token), json={"items": [{"product_id": product["id"], "quantity": 2}]})
    assert response.status_code == 201
    assert response.json()["total"] == round(product["price"] * 2, 2)
    after = next(p for p in client.get("/api/products").json() if p["id"] == product["id"])["stock"]
    assert after == before - 2

def test_customer_cannot_change_stock(client):
    customer_token = token(client, "customer", "ChangeMe_Customer_123!")
    product = client.get("/api/products").json()[0]
    response = client.patch(f"/api/products/{product['id']}/stock?stock=999", headers=auth(customer_token))
    assert response.status_code == 403

def test_order_requires_authentication(client):
    response = client.post("/api/orders", json={"items": [{"product_id": 1, "quantity": 1}]})
    assert response.status_code == 401

def test_insufficient_stock_is_rejected(client):
    customer_token = token(client, "customer", "ChangeMe_Customer_123!")
    product = client.get("/api/products").json()[0]
    response = client.post("/api/orders", headers=auth(customer_token), json={"items": [{"product_id": product["id"], "quantity": 999999}]})
    assert response.status_code in (409, 422)

def test_admin_summary_forbidden_to_customer(client):
    customer_token = token(client, "customer", "ChangeMe_Customer_123!")
    assert client.get("/api/admin/summary", headers=auth(customer_token)).status_code == 403
