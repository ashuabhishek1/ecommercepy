from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Numeric, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
import os, requests, uuid

DATABASE_URL=os.getenv("DATABASE_URL")
ORDER_URL=os.getenv("ORDER_URL")

engine=create_engine(DATABASE_URL)
with engine.connect() as conn: conn.execute(text(open("db/schema.sql").read())); conn.commit()

Base=declarative_base()
SessionLocal=sessionmaker(bind=engine)

class Transaction(Base):
    __tablename__="transactions"; __table_args__={"schema":"payment"}
    tx_id=Column(UUID(as_uuid=True), primary_key=True)
    order_id=Column(UUID(as_uuid=True), nullable=False)
    amount=Column(Numeric(10,2), nullable=False)
    status=Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

app=FastAPI(title="Transaction Service")

@app.post("/transactions")
def create_transaction(order_id:str, amount:float):
    r=requests.get(f"{ORDER_URL}/orders/{order_id}")
    if r.status_code!=200: raise HTTPException(404,"Order not found")
    order=r.json()
    if abs(order["total"] - amount) > 0.01:
        raise HTTPException(400,"Amount mismatch")
    tid=uuid.uuid4(); db=SessionLocal()
    db.add(Transaction(tx_id=tid, order_id=uuid.UUID(order_id), amount=amount, status="CAPTURED"))
    db.commit(); return {"tx_id":str(tid),"status":"CAPTURED"}
