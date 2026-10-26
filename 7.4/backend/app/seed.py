from sqlalchemy.orm import Session
from .models import User, Product
from .security import hash_password
from . import config

def seed(db: Session):
    defaults = [
        (config.ADMIN_USERNAME, config.ADMIN_PASSWORD, "admin"),
        (config.WAREHOUSE_USERNAME, config.WAREHOUSE_PASSWORD, "warehouse"),
        (config.CUSTOMER_USERNAME, config.CUSTOMER_PASSWORD, "customer"),
    ]
    for username, password, role in defaults:
        if not db.query(User).filter_by(username=username).first():
            db.add(User(username=username, password_hash=hash_password(password), role=role))
    products = [
        ("SKU-1001", "Wireless Barcode Scanner", "USB/Bluetooth warehouse scanner", 89.99, 35),
        ("SKU-1002", "Thermal Shipping Labels", "Roll of 500 shipping labels", 18.50, 120),
        ("SKU-1003", "Packing Tape Bundle", "Six-pack heavy-duty packing tape", 12.99, 75),
        ("SKU-1004", "Industrial Handheld Terminal", "Rugged inventory terminal", 349.00, 12),
        ("SKU-1005", "Shipping Scale", "Digital parcel scale up to 50 kg", 64.95, 20),
    ]
    for sku, name, description, price, stock in products:
        if not db.query(Product).filter_by(sku=sku).first():
            db.add(Product(sku=sku, name=name, description=description, price=price, stock=stock))
    db.commit()
