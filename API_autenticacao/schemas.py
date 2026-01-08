from pydantic import BaseModel, EmailStr
from typing import Optional

class UtilizadorSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str
    admin: Optional[bool] = False
