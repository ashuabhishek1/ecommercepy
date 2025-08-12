from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import declarative_base, sessionmaker
import os, requests

DATABASE_URL = os.getenv("DATABASE_URL")
PRODUCT_URL = os.getenv("PRODUCT_URL")

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text(open("db/schema.sql").read()))
    conn.commit()

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class CartLine(Base):
    __tablename__ = "cartlines"
    __table_args__ = {"schema": "cart"}
    cart_id = Column(String, primary_key=True)
    sku = Column(String, primary_key=True)
    qty = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)

class CartIn(BaseModel):
    cart_id: str
    sku: str
    qty: int

app = FastAPI(title="Cart Service")

@app.post("/carts/add")
def add_to_cart(line: CartIn):
    # Validate product exists
    r = requests.get(f"{PRODUCT_URL}/products/{line.sku}")
    if r.status_code != 200:
        raise HTTPException(status_code=404, detail="Product not found")
    db = SessionLocal()
    db.merge(CartLine(**line.dict()))
    db.commit()
    return {"message": "Item added to cart"}

@app.get("/carts/{cid}")
def get_cart(cid: str):
    db = SessionLocal()
    items = db.query(CartLine).filter_by(cart_id=cid).all()
    return {"cart_id": cid, "items": [{"sku": i.sku, "qty": i.qty} for i in items]}
