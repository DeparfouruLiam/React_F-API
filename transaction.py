from sqlmodel import Field, SQLModel
from datetime import timezone,datetime

created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)

class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    ibanSender: str = Field(index=True)
    ibanReceiver: str = Field(index=True)
    amount: int = Field(index=True)
    cancelled: bool = Field(default=False, index=True)
    date: datetime = Field(default=datetime.now(timezone.utc), index=True)