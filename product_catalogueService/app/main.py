from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Numeric, text
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    conn.execute(text(open("db/schema.sql").read()))
    conn.commit()

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "product"}
    sku = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    description = Column(String)

Base.metadata.create_all(bind=engine)

class ProductIn(BaseModel):
    sku: str
    name: str
    price: float
    description: str | None = None

app = FastAPI(title="Product Catalogue Service")

@app.post("/products")
def add_product(product: ProductIn):
    db = SessionLocal()
    if db.query(Product).filter_by(sku=product.sku).first():
        raise HTTPException(status_code=400, detail="Product exists")
    db.add(Product(**product.dict()))
    db.commit()
    return {"message": "Product added"}

@app.get("/products/{sku}")
def get_product(sku: str):
    db = SessionLocal()
    p = db.query(Product).filter_by(sku=sku).first()
    if not p:
        raise HTTPException(status_code=404, detail="Not found")
    return {"sku": p.sku, "name": p.name, "price": float(p.price), "description": p.description}
