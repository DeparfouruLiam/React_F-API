from sqlmodel import Field, SQLModel
from account import Account
from beneficiary import Beneficiary
import os
import hashlib
import binascii
import hmac

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str = Field(index=True)



CurrentUserId = 0
CurrentUserName = ""

def update_current_id(new_id):
    global CurrentUserId
    CurrentUserId = new_id

def update_current_name(new_name):
    global CurrentUserName
    CurrentUserName = new_name
def hash_password(password):
    if not isinstance(password, str):
        raise TypeError("password must be a string")
    salt = os.urandom(16)  # 128-bit salt
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt,  100_000)
    return f"{ 100_000}${binascii.hexlify(salt).decode()}${binascii.hexlify(dk).decode()}"

def getCurrentUserId():
    return CurrentUserId

def getCurrentUserName():
    return CurrentUserName

CurrentUser = 0

def get_current_user():
    return CurrentUser

def update_current_user(new_user):
    global CurrentUser
    CurrentUser = new_user
    return CurrentUser

def verify_password(stored_hash: str, password_attempt: str) -> bool:
    try:
        iterations_str, salt_hex, hash_hex = stored_hash.split('$')
        iterations = int(iterations_str)
        salt = binascii.unhexlify(salt_hex)
        expected_hash = binascii.unhexlify(hash_hex)
    except Exception:
        return False

    derived = hashlib.pbkdf2_hmac('sha256', password_attempt.encode('utf-8'), salt, iterations)
    return hmac.compare_digest(derived, expected_hash)
