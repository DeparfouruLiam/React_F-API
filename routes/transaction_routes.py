from datetime import  timedelta, timezone, datetime
from threading import Thread
import time
from fastapi import APIRouter, HTTPException, Depends

from account import Account, get_current_account
from database import get_session
from transaction import Transaction
from pydantic import BaseModel
router = APIRouter(prefix="/transaction", tags=["Transaction"])


@router.get("/transactions/{iban}")
def get_transactions_for_account(iban: str, session = Depends(get_session)):
    transactions = session.query(Transaction).filter(
        (Transaction.ibanSender == iban) |
        (Transaction.ibanReceiver == iban)
    ).order_by(Transaction.date.desc()).all()

    return {"transactions": transactions}

class AddMoneyRequest(BaseModel):
    amount: float
    iban: str

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
    sender = session.query(Account).filter_by(iban=body.sender_iban).first()
    if sender is None:
        raise HTTPException(status_code=404, detail="Sender account not found")

    # Validate receiver IBAN
    receiver = session.query(Account).filter_by(iban=body.receiver_iban).first()
    if receiver is None:
        raise HTTPException(status_code=404, detail="Receiver account not found")

    if sender.iban == receiver.iban:
        raise HTTPException(status_code=400, detail="Cannot transfer to same account")

    if body.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")

    if body.amount > sender.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    # Apply transaction
    sender.amount -= body.amount
    receiver.amount += body.amount

    # --- ADD THIS: CREATE TRANSACTION RECORD ---
    transaction = Transaction(
        ibanSender=sender.iban,
        ibanReceiver=receiver.iban,
        amount=body.amount,
        date=datetime.utcnow(),   # or use datetime.now(timezone.utc) if you prefer
        cancelled=False
    )
    session.add(transaction)

    # Commit everything
    session.commit()
    session.refresh(transaction)  # optional, ensures transaction.id is available

    return {
        "message": "Transfer successful",
        "sender_new_amount": sender.amount,
        "receiver_new_amount": receiver.amount,
        "transaction_id": transaction.id    # optional, useful for frontend
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
