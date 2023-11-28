from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from api.auth.router import router as auth_router
from api.common.validation import (
    validation_exception_handler, pydantic_exception_handler
)

from config.allowed_origins import ALLOWED_ORIGINS
from database.connection import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


app.add_exception_handler(ValidationError, pydantic_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

