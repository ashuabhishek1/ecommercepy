from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Numeric, Text, text
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
with engine.connect() as conn: conn.execute(text(open("db/schema.sql").read())); conn.commit()

Base=declarative_base()
SessionLocal=sessionmaker(bind=engine)

class Index(Base):
    __tablename__="index"; __table_args__={"schema":"search"}
    sku=Column(String, primary_key=True)
    name=Column(String, nullable=False)
    description=Column(Text)
    price=Column(Numeric(10,2))

Base.metadata.create_all(bind=engine)

class IndexIn(BaseModel):
    sku:str; name:str; description:str|None=None; price:float|None=None

app=FastAPI(title="Search Service")

@app.post("/index")
def add_product(doc:IndexIn):
    db=SessionLocal(); db.merge(Index(**doc.dict())); db.commit()
    return {"message":"indexed"}

@app.get("/search")
def search(q:str):
    db=SessionLocal()
    results=db.query(Index).filter(Index.name.ilike(f"%{q}%")).all()
    return [{"sku":r.sku,"name":r.name,"price":float(r.price) if r.price else None} for r in results]
