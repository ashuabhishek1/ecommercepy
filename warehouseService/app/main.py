from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, text
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
with engine.connect() as conn: conn.execute(text(open("db/schema.sql").read())); conn.commit()

Base=declarative_base()
SessionLocal=sessionmaker(bind=engine)

class Stock(Base):
    __tablename__="stock"; __table_args__={"schema":"warehouse"}
    sku=Column(String, primary_key=True)
    location=Column(String, nullable=False, default='MAIN')
    quantity=Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)

class StockIn(BaseModel):
    sku:str; quantity:int; location:str|None="MAIN"

app=FastAPI(title="Warehouse Service")

@app.post("/stock")
def set_stock(body:StockIn):
    db=SessionLocal(); db.merge(Stock(**body.dict())); db.commit()
    return {"message":"ok"}

@app.get("/stock/{sku}")
def get_stock(sku:str):
    db=SessionLocal(); s=db.query(Stock).filter_by(sku=sku).first()
    if not s: raise HTTPException(404,"Not found")
    return {"sku":s.sku,"location":s.location,"quantity":s.quantity}
