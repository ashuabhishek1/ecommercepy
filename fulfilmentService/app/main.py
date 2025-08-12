from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
import os, requests, uuid

DATABASE_URL=os.getenv("DATABASE_URL")
ORDER_URL=os.getenv("ORDER_URL")
WAREHOUSE_URL=os.getenv("WAREHOUSE_URL")
SHIPPING_URL=os.getenv("SHIPPING_URL")

engine=create_engine(DATABASE_URL)
with engine.connect() as conn: conn.execute(text(open("db/schema.sql").read())); conn.commit()

Base=declarative_base()
SessionLocal=sessionmaker(bind=engine)

class Job(Base):
    __tablename__="jobs"; __table_args__={"schema":"fulfilment"}
    job_id=Column(UUID(as_uuid=True), primary_key=True)
    order_id=Column(UUID(as_uuid=True), nullable=False)
    status=Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

class FulfilIn(BaseModel):
    order_id:str
    address:str

app=FastAPI(title="Fulfilment Service")

@app.post("/fulfil")
def fulfil_order(body:FulfilIn):
    ord_resp=requests.get(f"{ORDER_URL}/orders/{body.order_id}")
    if ord_resp.status_code!=200:
        raise HTTPException(404,"Order not found")
    ord_data=ord_resp.json()
    for item in ord_data.get("items",[]):
        stock=requests.get(f"{WAREHOUSE_URL}/stock/{item['sku']}")
        if stock.status_code!=200:
            raise HTTPException(400,f"SKU {item['sku']} not in stock")
        st_data=stock.json()
        if st_data["quantity"] < item["qty"]:
            raise HTTPException(409,f"Insufficient stock for {item['sku']}")
    ship=requests.post(f"{SHIPPING_URL}/shipments",json={"order_id":body.order_id,"address":body.address})
    if ship.status_code!=200:
        raise HTTPException(500,"Shipment creation failed")
    jid=uuid.uuid4(); db=SessionLocal()
    db.add(Job(job_id=jid, order_id=uuid.UUID(body.order_id), status="CREATED"))
    db.commit()
    return {"job_id":str(jid),"shipment":ship.json()}
