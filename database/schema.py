import datetime
from typing import Union

from pydantic import BaseModel


class Message(BaseModel):
    id: int
    sendTime: datetime.datetime
    sendStatus: bool
    clientId: int
    mailingId: int

    class Config:
        orm_mode = True


class Mailing(BaseModel):
    id: int
    messageText: Union[str, None] = None
    startDate: datetime.datetime
    endDate: datetime.datetime
    clientsTag: Union[str, None] = None
    clientsPhoneCode: Union[str, None] = None
    messages: list[Message] = []

    class Config:
        orm_mode = True
