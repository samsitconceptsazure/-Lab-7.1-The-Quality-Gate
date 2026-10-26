from pydantic import BaseModel, Field, ConfigDict

class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=1, max_length=200)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class ProductCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=1, max_length=160)
    description: str = Field(default="", max_length=500)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    sku: str
    name: str
    description: str
    price: float
    stock: int

class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, le=1000)

class OrderCreate(BaseModel):
    items: list[OrderItemIn] = Field(min_length=1, max_length=50)

class OrderItemOut(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float

class OrderOut(BaseModel):
    id: int
    customer_username: str
    status: str
    total: float
    created_at: str | None = None
    items: list[OrderItemOut]
