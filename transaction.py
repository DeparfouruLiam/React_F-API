from sqlmodel import Field, SQLModel
from typing import TypedDict
from datetime import *
import config

created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)


# class Transaction:
#     ibanSender: str
#     ibanReceiver: str
#     amount: int
#     cancelled: bool = False
#     id:int
#     date: datetime
#
#     def __init__(self, iban_sender: str, iban_receiver: str, amount: int) -> None:
#         self.cancelled = None
#         self.ibanSender = iban_sender
#         self.ibanReceiver = iban_receiver
#         self.amount = amount
#         self.date = datetime.now(timezone.utc)
#         self.id = config.transactionCount
#         config.transactionCount += 1

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ibanSender: str = Field(index=True)
    ibanReceiver: str = Field(index=True)
    amount: int = Field(index=True)
    cancelled: bool = Field(default=False, index=True)
    date: datetime = Field(default=datetime.now(timezone.utc), index=True)

#All transactions
# TransactionLG= Transaction("Aled", "Yiouiuh", 20)