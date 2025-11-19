from fastapi import APIRouter, HTTPException, Depends
from account import *
from database import get_session
from routes.user_routes import get_user, me
from user import CurrentUser, get_current_user, getCurrentUserId, User
from pydantic import BaseModel

router = APIRouter(prefix="/accounts", tags=["Accounts"])

class CreateAccount(BaseModel):
    iban: str

@router.get("/goofy")
def goofy():
    return {"message": "AAAAAAAAAAAA"}

@router.get("/current_account_amount")
def read_amount(user=Depends(get_user), session = Depends(get_session)):
    user_id = session.query(User).filter_by(username=user["username"]).first().id
    account = get_iban()
    if account is "":
        return {"Amount": "No account linked to this IBAN"}
    amount = session.query(Account).filter_by(user_id=user_id).first()
    return {"Amount": amount.amount}

@router.get("/choose_current_account")
def choose_current_account(iban, user=Depends(get_user), session=Depends(get_session)):
    user_id = session.query(User).filter_by(username=user["username"]).first().id
    if user_id is 0:
        return {"Not connected"}
    new_account = session.query(Account).filter_by(iban=iban).first()
    if new_account is None:
        return {"No account linked to this IBAN in your accounts"}
    update_account_id(new_account.id)
    return {"Current account successfully updated to": new_account.iban}

@router.post("/create_account", response_model=CreateAccount)
def create_account(body: CreateAccount, user=Depends(get_user), session = Depends(get_session)) -> Account:
    user_id = me()["user_id"]
    if user_id == 0:
        raise HTTPException(status_code=404, detail="User not connected")
    account = Account(amount=100, iban=body.iban, user_id=user_id)
    session.add(account)
    session.commit()
    session.refresh(account)
    return account

@router.get("/current_account")
def get_my_account():
    return {"Iban": get_iban()}
