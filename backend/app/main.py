from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import text
from .database import Base, engine, get_db
from .models import User, Product, Order, OrderItem
from .schemas import LoginRequest, TokenResponse, ProductOut, ProductCreate, OrderCreate
from .security import verify_password, create_token, current_user, require_roles
from .seed import seed

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    try:
        seed(db)
    finally:
        db.close()
    yield

app = FastAPI(title="RetailOps Order Management API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/health")
def health():
    return {"status": "healthy", "service": "retailops-api"}

@app.get("/ready")
def ready(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ready", "database": "connected"}

@app.post("/api/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return TokenResponse(access_token=create_token(user.username, user.role), role=user.role)

@app.get("/api/auth/me")
def me(user: User = Depends(current_user)):
    return {"username": user.username, "role": user.role}

@app.get("/api/products", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.id).all()

@app.post("/api/products", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "warehouse"))):
    if db.query(Product).filter_by(sku=data.sku).first():
        raise HTTPException(status_code=409, detail="SKU already exists")
    product = Product(sku=data.sku, name=data.name, description=data.description, price=data.price, stock=data.stock)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.patch("/api/products/{product_id}/stock")
def update_stock(product_id: int, stock: int, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "warehouse"))):
    if stock < 0:
        raise HTTPException(status_code=422, detail="Stock cannot be negative")
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stock = stock
    db.commit()
    return {"id": product.id, "stock": product.stock}

@app.post("/api/orders", status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db), user: User = Depends(current_user)):
    # Combine duplicate product IDs so stock validation and decrement are consistent.
    quantities = {}
    for item in data.items:
        quantities[item.product_id] = quantities.get(item.product_id, 0) + item.quantity
    products = {}
    for product_id, quantity in quantities.items():
        product = db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        if product.stock < quantity:
            raise HTTPException(status_code=409, detail=f"Insufficient stock for {product.name}")
        products[product_id] = (product, quantity)
    total = sum(product.price * quantity for product, quantity in products.values())
    order = Order(customer_username=user.username, status="PLACED", total=round(total, 2))
    for product, quantity in products.values():
        product.stock -= quantity
        order.items.append(OrderItem(product_id=product.id, product_name=product.name, quantity=quantity, unit_price=product.price))
    db.add(order)
    db.commit()
    db.refresh(order)
    return {"id": order.id, "customer_username": order.customer_username, "status": order.status, "total": order.total, "items": [{"product_id": i.product_id, "product_name": i.product_name, "quantity": i.quantity, "unit_price": i.unit_price} for i in order.items]}

@app.get("/api/orders")
def list_orders(db: Session = Depends(get_db), user: User = Depends(current_user)):
    query = db.query(Order).options(joinedload(Order.items)).order_by(Order.id.desc())
    if user.role == "customer":
        query = query.filter(Order.customer_username == user.username)
    orders = query.all()
    return [{"id": o.id, "customer_username": o.customer_username, "status": o.status, "total": o.total, "created_at": o.created_at.isoformat() if o.created_at else None, "items": [{"product_id": i.product_id, "product_name": i.product_name, "quantity": i.quantity, "unit_price": i.unit_price} for i in o.items]} for o in orders]

@app.patch("/api/orders/{order_id}/status")
def update_order_status(order_id: int, status_value: str, db: Session = Depends(get_db), user: User = Depends(require_roles("admin", "warehouse"))):
    allowed = {"PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"}
    if status_value not in allowed:
        raise HTTPException(status_code=422, detail=f"Status must be one of {sorted(allowed)}")
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status in {"DELIVERED", "CANCELLED"}:
        raise HTTPException(status_code=409, detail="Terminal orders cannot be changed")
    if status_value == "CANCELLED":
        for item in order.items:
            product = db.get(Product, item.product_id)
            if product:
                product.stock += item.quantity
    order.status = status_value
    db.commit()
    return {"id": order.id, "status": order.status}

@app.get("/api/admin/summary")
def admin_summary(db: Session = Depends(get_db), user: User = Depends(require_roles("admin"))):
    return {
        "products": db.query(Product).count(),
        "orders": db.query(Order).count(),
        "users": db.query(User).count(),
        "inventory_units": sum(p.stock for p in db.query(Product).all()),
    }
