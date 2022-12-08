from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from .database import Base


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    phone = Column(String)
    phoneCode = Column(String)
    tag = Column(String)
    utc = Column(String)
    messages = relationship("Message", backref=backref("clients"))


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    sendTime = Column(DateTime)
    sendStatus = Column(Boolean, default=False)
    clientId = Column(Integer, ForeignKey("clients.id"))
    mailingId = Column(Integer, ForeignKey("mailings.id"))
    mailing = relationship("Mailing", back_populates="messages")


class Mailing(Base):
    __tablename__ = "mailings"
    id = Column(Integer, primary_key=True)
    startDate = Column(DateTime)
    messageText = Column(String)
    clientsTag = Column(String)
    clientsPhoneCode = Column(String)
    endDate = Column(DateTime)

    messages = relationship("Message", back_populates="mailing")
