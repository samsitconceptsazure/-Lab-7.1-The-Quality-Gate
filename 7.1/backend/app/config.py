import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./retailops_test.db",
)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "local-test-secret-change-this-before-deploying")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "ChangeMe_Admin_123!")
WAREHOUSE_USERNAME = os.getenv("WAREHOUSE_USERNAME", "warehouse")
WAREHOUSE_PASSWORD = os.getenv("WAREHOUSE_PASSWORD", "ChangeMe_Warehouse_123!")
CUSTOMER_USERNAME = os.getenv("CUSTOMER_USERNAME", "customer")
CUSTOMER_PASSWORD = os.getenv("CUSTOMER_PASSWORD", "ChangeMe_Customer_123!")
