from sqlmodel import Field, SQLModel
from typing import TypedDict
from transaction import *

class Account(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    amount: int = Field(index=True)
    iban: str = Field(index=True)
    user_id: int = Field(index=True)
    is_main: bool = Field(default=False, index=True)
#All accounts
# LiamAccount = Account (100, "Aled", [TransactionLG])
# GhaziAccount = Account (10, "Yiouiuh", [TransactionLG])
# AdamAccount = Account (50, "Buranyah", [])

# CurrentAccount = Account (0,  "",  [])
#
# accounts = [LiamAccount, GhaziAccount, AdamAccount]

CurrentAccountId = 0
CurrentAmount = 0
CurrentIban = ""

def update_account_id(new_id):
    global CurrentAccountId
    CurrentAccountId = new_id

def update_amount(new_amount):
    global CurrentAmount
    CurrentAmount = new_amount

def update_iban(new_iban):
    global CurrentIban
    CurrentIban = new_iban

def get_account_id():
    global CurrentAccountId
    return CurrentAccountId

def get_amount():
    global CurrentAmount
    return CurrentAmount

def get_iban():
    global CurrentIban
    return CurrentIban


def get_current_account():
    return CurrentAccount

# def add_account(iban: str):
#     new_account = Account(0, iban, [])
#     accounts.append(new_account)
#     return new_account

def update_current_account(new_account):
    global CurrentAccount
    CurrentAccount = new_account
    return CurrentAccount

# def account_from_iban(iban):
#     return next((x for x in get_accounts() if x.get_iban() == iban), None)

def user_account_from_iban(iban,user_accounts):
    return next((x for x in user_accounts if x.get_iban() == iban), None)