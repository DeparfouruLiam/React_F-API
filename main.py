from typing import TypedDict
from fastapi import FastAPI, Depends
from routes import account_routes,user_routes,transaction_routes,beneficiary_routes
import asyncio
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import JWTError, jwt



from database import create_db_and_tables
from routes import account_routes, user_routes, transaction_routes, beneficiary_routes, database_routes

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(title="Gooning Factory API")

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/goofy")
def goofy():
    return {"message": "AAAAAAAAAAAA"}




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def periodic_task():
    while True:
        # Put your actual function code here
        await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_task())


app.include_router(account_routes.router)
app.include_router(user_routes.router)
app.include_router(transaction_routes.router)
app.include_router(beneficiary_routes.router)

app.include_router(database_routes.router)