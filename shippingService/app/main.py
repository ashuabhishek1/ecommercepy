from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Text, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
import os, requests, uuid

DATABASE_URL=os.getenv("DATABASE_URL")
ORDER_URL=os.getenv("ORDER_URL")
engine=create_engine(DATABASE_URL)
with engine.connect() as conn: conn.execute(text(open("db/schema.sql").read())); conn.commit()

Base=declarative_base()
SessionLocal=sessionmaker(bind=engine)

class Shipment(Base):
    __tablename__="shipments"; __table_args__={"schema":"shipping"}
    shipment_id=Column(UUID(as_uuid=True), primary_key=True)
    order_id=Column(UUID(as_uuid=True), nullable=False)
    address=Column(Text, nullable=False)
    status=Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

class ShipmentIn(BaseModel):
    order_id:str; address:str

app=FastAPI(title="Shipping Service")

@app.post("/shipments")
def create_shipment(body:ShipmentIn):
    if requests.get(f"{ORDER_URL}/orders/{body.order_id}").status_code!=200:
        raise HTTPException(404,"Order not found")
    sid=uuid.uuid4(); db=SessionLocal()
    db.add(Shipment(shipment_id=sid, order_id=uuid.UUID(body.order_id), address=body.address, status="CREATED"))
    db.commit()
    return {"shipment_id":str(sid),"status":"CREATED"}
