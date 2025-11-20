from datetime import  timedelta, timezone, datetime
from threading import Thread
import time
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from account import *
from database import get_session
from user import *
import config
from pydantic import BaseModel

class AddMoneyRequest(BaseModel):
    amount: float
    iban: str
router = APIRouter(prefix="/transaction", tags=["Transaction"])

class CreateTransaction(BaseModel):
    sender_iban: str
    receiver_iban: str
    amount: int

@router.post("/add_money")
def add_money(body: AddMoneyRequest, session = Depends(get_session)):
     if body.amount <= 0:
         raise HTTPException(status_code=400, detail="Amount must be positive")
     iban = body.iban
     if not iban:
         raise HTTPException(status_code=400, detail="Not connected to an account")
     account = session.query(Account).filter_by(iban=iban).first()
     if not account:
         raise HTTPException(status_code=404, detail="Account not found")
     account.amount += body.amount
     session.commit()
     return {
         "message": "Money added successfully",
         "iban": account.iban,
         "new_amount": account.amount
     }
@router.post("/transfer")
def transfer_amount(body: CreateTransaction, session = Depends(get_session)):

    # Validate sender IBAN
    if body.sender_iban == "":
        raise HTTPException(status_code=400, detail="Not connected to an account")
    # Fetch sender account
    sender = session.query(Account).filter_by(iban=body.sender_iban).first()
    if sender is None:
        raise HTTPException(status_code=404, detail="Sender account not found")
    # Fetch receiver account
    receiver = session.query(Account).filter_by(iban=body.receiver_iban).first()
    if receiver is None:
        raise HTTPException(status_code=404, detail="Receiver account not found")
    # Prevent self-transfer
    if sender.iban == receiver.iban:
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")
    # Validate amount
    if body.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    # Check balance
    if body.amount > sender.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    # Apply transaction
    sender.amount -= body.amount
    receiver.amount += body.amount
    # Save changes
    session.commit()
    return {
        "message": "Transfer successful",
        "sender_new_amount": sender.amount,
        "receiver_new_amount": receiver.amount
    }
def create_thread(trs: dict, session = Depends(get_session)):
    transaction = Transaction(ibanSender=trs.get("sender_iban"),ibanReceiver=trs.get("receiver_iban"), amount=trs.get("amount"))
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    thread = Thread(target=check_flag_later, args=(transaction.id, session))
    thread.start()
    return {"message": "Object created and background check started."}

def check_flag_later(id_transaction:int , session = Depends(get_session)):
    time.sleep(5)
    print(id_transaction)
    transaction = session.query(Transaction).filter_by(id=id_transaction).first()
    if not transaction.cancelled :
        session.query(Account).filter_by(iban=transaction.ibanSender).first().amount -= transaction.amount
        session.query(Account).filter_by(iban=transaction.ibanReceiver).first().amount += transaction.amount
        session.commit()
        session.refresh(transaction)
        print("Flag is still False after 5 seconds!")
    else:
        print("Flag was set to True before 5 seconds.")

@router.get("/cancelTransaction")
def cancel_transaction():
    i:int  =0
    for transaction in get_current_account().get_transactions() :
        if transaction.ibanSender  == get_current_account().iban :
            if transaction.ibanReceiver  != get_current_account().iban :
                if not transaction.cancelled:
                    if datetime.now(timezone.utc) - transaction.date.replace(tzinfo=timezone.utc) <= timedelta(seconds=10):
                        get_current_account().transactions[i].cancelled=True
                        return transaction.ibanReceiver ,transaction.ibanSender ,transaction.amount ,datetime.now(timezone.utc) - transaction.date .replace(tzinfo=timezone.utc)
        i=i+1
    return  datetime.now(timezone.utc)

@router.get("/ShowTransaction")
def show_transaction():
    current_account = get_current_account()
    return {"transactions": current_account.get_transactions()}
