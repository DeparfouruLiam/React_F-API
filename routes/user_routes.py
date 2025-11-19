from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from account import *
from beneficiary import Beneficiary
from database import get_session
from user import *
from newclass import *
from fastapi import APIRouter, HTTPException,Depends,status,Form
from pydantic import BaseModel

from user import *
from auth import *
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status


bearer_scheme = HTTPBearer()
router = APIRouter(prefix="/user", tags=["User"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Login")

import jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

secret_key = "very_secret_key"
algorithm = "HS256"
security = HTTPBearer()

class CreateUser(BaseModel):
    username: str
    password: str

class CreateAccount(BaseModel):
    iban: str

def get_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    try:
        payload = jwt.decode(credentials.credentials, secret_key, algorithms=[algorithm])
        return payload  # You can also return a user object or dict here
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
def generate_token(user: CreateUser):
    return jwt.encode(user.dict(), secret_key, algorithm=algorithm)

@router.get("/test")
def test():
    me()
@router.post("/register")
def register_user(body: CreateUser,body_account:CreateAccount, session = Depends(get_session)) -> str:
    user = session.query(User).filter_by(username=body.username).first()
    if user:
        raise HTTPException(status_code=404, detail="Username already used")
    user = User(username=body.username, password=body.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    account = Account(amount=100, iban=body_account.iban, user_id=user.id, is_main=True)
    session.add(account)
    session.commit()
    session.refresh(account)
    login(CreateUser(username=body.username, password=body.password),session)
    return "Account created"

@router.post("/login")
def login(user: CreateUser, session = Depends(get_session)):
    current_user = session.query(User).filter_by(username=user.username).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    main_account = session.query(Account).filter_by(user_id=current_user.id, is_main=True).first()

    update_iban(main_account.iban)
    update_account_id(main_account.id)
    update_amount(main_account.amount)

    update_current_id(current_user.id)
    update_current_name(current_user.username)

    return {"token": generate_token(user)}

@router.get("/meme")
def me(user=Depends(get_user)):
    return user



@router.get("/current_user")
def get_my_user(user=Depends(get_user), session = Depends(get_session)):
    user_id = session.query(User).filter_by(username=user["username"]).first().id
    return {"ID": user_id,"username": user["username"]}

@router.get("/get_all_accounts")
def get_all_accounts(user=Depends(get_user), session = Depends(get_session)):
    ibans = ""
    user_id = session.query(User).filter_by(username=user["username"]).first().id
    all_accounts = session.query(Account).filter_by(user_id=user_id).all()
    for x in all_accounts:
        ibans += x.iban+" : "+str(x.amount)+" zennys ; "
    return {"All your accounts are": ibans}

class CreateBeneficiary(BaseModel):
    username: str
    iban: str

@router.post("/add_beneficiary", response_model=CreateBeneficiary)
def add_Beneficiary(body: CreateBeneficiary, user=Depends(get_user), session = Depends(get_session)) -> Beneficiary | None:
    user_id = session.query(User).filter_by(username=user["username"]).first().id
    if not session.query(Account).filter_by(iban=body.iban).first() is None: #chercher avec bdd
        #for bene in get_current_user().get_beneficiaries():
            #if bene.get_iban() == iban:
                #return "Beneficiary already exists"

        beneficiary = Beneficiary(username=body.username, iban=body.iban, user_id=user_id)
        session.add(beneficiary)
        session.commit()
        session.refresh(beneficiary)

        #beneficiary = Beneficiary(iban, name)
        #get_current_user().add_beneficiaries(beneficiary)
        return  beneficiary
    return None


# @router.post("/create_account", response_model=CreateAccount)
# def create_account(body: CreateAccount, user=Depends(get_user), session = Depends(get_session)) -> Account:
#     user_id = session.query(User).filter_by(username=user["username"]).first().id
#     if user_id == 0:
#         raise HTTPException(status_code=404, detail="User not connected")
#     account = Account(amount=100, iban=body.iban, user_id=user_id)
#     session.add(account)
#     session.commit()
#     session.refresh(account)
#     return account


@router.get("/showBeneficiary")
def show_Beneficiary(user=Depends(get_user), session = Depends(get_session), response_model=CreateAccount):
    user_id = session.query(User).filter_by(username=user["username"]).first().id
    beneficiaries = ""
    all_beneficiaries = session.query(Beneficiary).filter_by(user_id=user_id).all()
    for x in all_beneficiaries:
        #user_name = session.query(User).filter_by(id=x.user_id).first().username
        beneficiaries += x.iban + ", id : " + str(x.id) + ", " + "User : " + x.username + "; "+"Datetime "+ str(x.created_at)
    return {"All your accounts are": beneficiaries}


