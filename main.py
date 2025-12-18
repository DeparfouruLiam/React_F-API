import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import account_routes, user_routes, transaction_routes, beneficiary_routes, database_routes
from database import create_db_and_tables

app = FastAPI(title="Gooning Factory API")

# Allowed origins
origins = [
    "http://backend:5173",
    "http://backend:3000",
    "http://127.0.0.1:5173",
    "http://backend:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(account_routes.router)
app.include_router(user_routes.router)
app.include_router(transaction_routes.router)
app.include_router(beneficiary_routes.router)
app.include_router(database_routes.router)

# Database initialization
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Example endpoint
@app.get("/goofy")
def goofy():
    return {"message": "AAAAAAAAAAAA"}

# Periodic task example
async def periodic_task():
    while True:
        await asyncio.sleep(10)  # Remplace par ton code réel

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(periodic_task())
