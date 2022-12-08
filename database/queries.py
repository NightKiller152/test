import datetime
from sqlalchemy.orm import Session
from . import models, schema


def get_clients(db: Session):
    return db.query(models.Client).all()


def get_client_by_phone(db: Session, phone: str):
    return db.query(models.Client).filter(models.Client.phone == phone).first()


def get_client_by_id(db: Session, id: int):
    return db.query(models.Client).filter(models.Client.id == id).first()


def get_mailing_by_id(db: Session, id: int):
    mailing = db.query(models.Mailing).filter(models.Mailing.id == id).first()
    return mailing


def get_messages_by_mailingId(db: Session, mailingId: int):
    return db.query(models.Message).filter(models.Message.mailingId == mailingId).all()


def create_client(db: Session, phone: str, tag: str, utc: str):
    client = models.Client(phone=phone, phoneCode=phone[0], tag=tag, utc=utc)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def create_mailing(db: Session, startDate: datetime.datetime, messageText: str, clientsTag: str, clientsPhoneCode: str,
                   endDate: datetime.datetime):
    mailing = models.Mailing(startDate=startDate, messageText=messageText, clientsTag=clientsTag,
                             clientsPhoneCode=clientsPhoneCode, endDate=endDate)
    db.add(mailing)
    db.commit()
    db.refresh(mailing)
    return mailing


def update_mailing(db: Session, id: int, startDate: datetime.datetime, messageText: str, clientsTag: str,
                   clientsPhoneCode: str, endDate: datetime.datetime):
    mailing = db.query(models.Mailing).filter(models.Mailing.id == id).first()
    mailing.messageText = messageText
    mailing.startDate = startDate
    mailing.clientsTag = clientsTag
    mailing.clientsPhoneCode = clientsPhoneCode
    mailing.endDate = endDate
    db.commit()
    db.refresh(mailing)
    return mailing


def update_client(db: Session, id: int, phone: str or None, tag: str or None, utc: str or None):
    client = db.query(models.Client).filter(models.Client.id == id).first()
    client.phone = phone
    client.tag = tag
    client.utc = utc
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, id: int):
    client = db.query(models.Client).filter(models.Client.id == id).first()
    db.delete(client)
    db.commit()
    return f"Client id: {id} deleted"


def delete_mailing(db: Session, id: int):
    mailing = db.query(models.Mailing).filter(models.Mailing.id == id).first()
    db.delete(mailing)
    db.commit()
    return f"Mailing id: {id} deleted"

