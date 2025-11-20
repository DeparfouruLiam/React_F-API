from fastapi import APIRouter, HTTPException, Depends
from account import *
from database import get_session
from routes.user_routes import get_user, me
from user import CurrentUser, get_current_user, getCurrentUserId, User
from pydantic import BaseModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security import OAuth2PasswordBearer

bearer_scheme = HTTPBearer()
router = APIRouter(prefix="/accounts", tags=["Accounts"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Login")

import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

secret_key = "very_secret_key"
algorithm = "HS256"
security = HTTPBearer()

class CreateAccount(BaseModel):
    iban: str

@router.get("/goofy")
def goofy():
    return {"message": "AAAAAAAAAAAA"}

@router.get("/current_account_amount")
def read_amount(user=Depends(get_user), session = Depends(get_session)):
    user_id = session.query(User).filter_by(username=user["username"]).first().id
    account = get_iban()
    if account == "":
        return {"Amount": "No account linked to this IBAN"}
    amount = session.query(Account).filter_by(user_id=user_id).first()
    return {"Amount": amount.amount}

@router.post("/choose_current_account")
def choose_current_account(body: CreateAccount, user=Depends(get_user), session=Depends(get_session)):
    user_id = session.query(User).filter_by(username=user["username"]).first().id
    if user_id == 0:
        return {"Not connected"}
    new_account = session.query(Account).filter_by(iban=body.iban).first()
    if new_account is None:
        return {"No account linked to this IBAN in your accounts"}
    update_account_id(new_account.id)
    update_iban(new_account.iban)
    update_amount(new_account.amount)
    return {"Current account successfully updated to": new_account.iban}

@router.post("/create_account", response_model=CreateAccount)
def create_account(body: CreateAccount, user=Depends(get_user), session = Depends(get_session)) -> Account:
    user_id = session.query(User).filter_by(username=user["username"]).first().id
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


@router.delete("/delete_account")
def delete_account(body: CreateAccount, user=Depends(get_user), session=Depends(get_session)):
    if user is None:
        raise HTTPException(status_code=401, detail="Not connected")

    ibans = []
    current_user = session.query(User).filter_by(username=user["username"]).first()
    user_id = current_user.id
    all_accounts = session.query(Account).filter_by(user_id=user_id).all()

    for x in all_accounts:
        ibans.append(x.iban)

    # Vérifie que le compte appartient bien à l'utilisateur
    if body.iban not in ibans:
        raise HTTPException(status_code=403, detail="You do not have an account linked to this IBAN")

    to_delete = session.query(Account).filter_by(iban=body.iban).first()

    if to_delete.is_main:
        raise HTTPException(status_code=403, detail="You cannot delete your main account")

    main_account = session.query(Account).filter_by(user_id=user_id, is_main=True).first()

    to_delete.activated = False
    main_account.amount += to_delete.amount
    to_delete.amount = 0

    session.commit()
    session.refresh(to_delete)

    update_account_id(main_account.id)

    return {"message": f"Account {body.iban} successfully deleted"}