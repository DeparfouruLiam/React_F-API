from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from database import *
from newclass import *
from user import *

router = APIRouter(prefix="/database", tags=["Database"])

