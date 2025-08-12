from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, String, Integer, Numeric, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
import os, requests, uuid

DATABASE_URL = os.getenv("DATABASE_URL")
CART_URL = os.getenv("CART_URL")
PRODUCT_URL = os.getenv("PRODUCT_URL")
CUSTOMER_URL = os.getenv("CUSTOMER_URL")

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text(open("db/schema.sql").read()))
    conn.commit()

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "orders"}
    order_id = Column(UUID(as_uuid=True), primary_key=True)
    cart_id = Column(String, nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    total = Column(Numeric(10,2), nullable=False)
    status = Column(String, nullable=False)

class OrderLine(Base):
    __tablename__ = "order_lines"
    __table_args__ = {"schema": "orders"}
    order_id = Column(UUID(as_uuid=True), primary_key=True)
    sku = Column(String, primary_key=True)
    qty = Column(Integer, nullable=False)
    price = Column(Numeric(10,2), nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Service")

@app.post("/orders")
def create_order(cart_id: str, customer_id: str):
    if requests.get(f"{CUSTOMER_URL}/customers/{customer_id}").status_code != 200:
        raise HTTPException(400, "Customer not found")
    cart_resp = requests.get(f"{CART_URL}/carts/{cart_id}")
    if cart_resp.status_code != 200:
        raise HTTPException(404, "Cart not found")
    cart_data = cart_resp.json()
    total=0; lines=[]
    for item in cart_data["items"]:
        pr = requests.get(f"{PRODUCT_URL}/products/{item['sku']}")
        if pr.status_code != 200:
            raise HTTPException(400,f"SKU {item['sku']} missing")
        pdata=pr.json()
        price=pdata["price"]
        total += price * item["qty"]
        lines.append((item["sku"],item["qty"],price))
    oid = uuid.uuid4()
    db = SessionLocal()
    db.add(Order(order_id=oid, cart_id=cart_id, customer_id=uuid.UUID(customer_id), total=total, status="NEW"))
    for sku, qty, price in lines:
        db.add(OrderLine(order_id=oid, sku=sku, qty=qty, price=price))
    db.commit()
    return {"order_id": str(oid), "total": float(total), "status": "NEW"}
