import datetime

from fastapi import FastAPI, Depends, HTTPException
from database import models, queries, schema
from typing import Union, List
from database.database import engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import DateTime

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/allClients")
async def get_all_clients(db: Session = Depends(get_db)):
    return queries.get_clients(db)


@app.get("/clients/phone={phone}")
async def get_client_by_phone(phone: str, db: Session = Depends(get_db)):
    client = queries.get_client_by_phone(db, phone=phone)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.get("/clients/id={id}")
async def get_client_by_id(id: int, db: Session = Depends(get_db)):
    client = queries.get_client_by_id(db, id=id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.get("/mailings/{id}", response_model=schema.Mailing)
async def get_mailing_by_id(id: int, db: Session = Depends(get_db)):
    mailing = queries.get_mailing_by_id(db, id=id)
    if mailing is None:
        raise HTTPException(status_code=404, detail="Mailing not found")
    return mailing


@app.post("/clients/create/phone={phone}&tag={tag}&utc={utc}")
async def create_client(phone: str, tag: str, utc: str, db: Session = Depends(get_db)):
    client = queries.get_client_by_phone(db, phone=phone)
    if client is not None:
        raise HTTPException(status_code=404, detail=f"Client with phone: {phone} already exists")
    return queries.create_client(db, phone, tag, utc)


@app.post("/mailings/create/{startDate}&{messageText}&{clientsTag}&{clientsPhoneCode}&{endDate}", response_model=schema.Mailing)
async def create_mailing(startDate: datetime.datetime, messageText: str, clientsTag: str, clientsPhoneCode: str, endDate: datetime.datetime,
                        db: Session = Depends(get_db)):
    return queries.create_mailing(db, startDate, messageText, clientsTag, clientsPhoneCode, endDate)


@app.post("/clients/update/{id}/")
async def update_client(id: int, phone: Union[str, None] = None, tag: Union[str, None] = None,
                        utc: Union[str, None] = None, db: Session = Depends(get_db)):

    client = queries.get_client_by_id(db, id=id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return queries.update_client(db, id, phone, tag, utc)


@app.post("/mailings/update/{id}/", response_model=schema.Mailing)
async def update_mailing(id: int, startDate: Union[datetime.datetime, None] = None, messageText: Union[str, None] = None,
                        clientsTag: Union[str, None] = None, clientsPhoneCode: Union[str, None] = None,
                        endDate: Union[datetime.datetime, None] = None, db: Session = Depends(get_db)):

    mailing = queries.get_mailing_by_id(db, id=id)
    if mailing is None:
        raise HTTPException(status_code=404, detail="Mailing not found")
    return queries.update_mailing(db, id, startDate, messageText, clientsTag, clientsPhoneCode, endDate)


@app.post("/clients/delete/{id}", response_model=str)
async def delete_client(id: int, db: Session = Depends(get_db)):
    client = queries.get_client_by_id(db, id=id)
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return queries.delete_client(db, id)


@app.post("/mailings/delete/{id}", response_model=str)
async def delete_client(id: int, db: Session = Depends(get_db)):
    mailing = queries.get_mailing_by_id(db, id=id)
    if mailing is None:
        raise HTTPException(status_code=404, detail="Mailing not found")
    return queries.delete_mailing(db, id)
