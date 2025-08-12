from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
import os, uuid

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
with engine.connect() as conn: conn.execute(text(open("db/schema.sql").read())); conn.commit()

Base=declarative_base()
SessionLocal=sessionmaker(bind=engine)

class Customer(Base):
    __tablename__="customers"; __table_args__={"schema":"customer"}
    customer_id=Column(UUID(as_uuid=True), primary_key=True)
    name=Column(String, nullable=False)
    email=Column(String, unique=True, nullable=False)
    phone=Column(String)

Base.metadata.create_all(bind=engine)

class CustomerIn(BaseModel):
    name:str
    email:EmailStr
    phone:str|None=None

app=FastAPI(title="Customer Service")

@app.post("/customers")
def create_customer(c:CustomerIn):
    db=SessionLocal()
    if db.query(Customer).filter_by(email=c.email).first():
        raise HTTPException(400,"Email exists")
    cid=uuid.uuid4()
    db.add(Customer(customer_id=cid, **c.dict()))
    db.commit()
    return {"customer_id":str(cid)}

@app.get("/customers/{cid}")
def get_customer(cid:str):
    db=SessionLocal(); cust=db.query(Customer).filter_by(customer_id=cid).first()
    if not cust: raise HTTPException(404,"Not found")
    return {"customer_id":str(cust.customer_id),"name":cust.name,"email":cust.email,"phone":cust.phone}
