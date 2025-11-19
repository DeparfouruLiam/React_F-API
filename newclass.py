# from sqlmodel import Field, SQLModel
# from datetime import datetime, timedelta, UTC, timezone
#
# class Transaction(SQLModel, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     ibanSender: str = Field(index=True)
#     ibanReceiver: str = Field(index=True)
#     amount: int = Field(index=True)
#     cancelled: bool = Field(default=False, index=True)
#     date: datetime = Field(default=None, index=True)

# class Transaction:
#     ibanSender: str
#     ibanReceiver: str
#     amount: int
#     cancelled: bool = False
#     id:int
#     date: datetime