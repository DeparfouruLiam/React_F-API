from datetime import  timedelta, timezone, datetime
from threading import Thread
import time
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from account import *
from database import get_session
from user import *
import config

router = APIRouter(prefix="/transaction", tags=["Transaction"])

class CreateTransaction(BaseModel):
    receiver_iban: str
    amount: int

@router.post("/transfer")
def transfer_amount(body: CreateTransaction, session = Depends(get_session)):
    if get_iban() is "":
        return {"Not connected to an account"}
    receiver = session.query(Account).filter_by(iban=body.receiver_iban).first()
    if receiver is None:
        return {"No account linked to the IBAN of the receiver"}
    if get_iban() is receiver.iban:
        return {"Transfer must be from one account to another"}
    if body.amount > get_amount():
        return {"Sender doesn't have enough to transfer the amount"}
    current_transaction = {"sender_iban":get_iban(),"receiver_iban": receiver.iban,"amount": body.amount}

    config.transactionCount+=1
    create_thread(current_transaction, session)

    return {"The transfer was successful. "+get_iban()+" new amount": get_amount(), receiver.iban+" new amount": receiver.amount}

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
