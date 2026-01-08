from fastapi import FastAPI
from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

app = FastAPI()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oath2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login-form")

from auth_routes import auth_router

app.include_router(auth_router)
