from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from jose import jwt
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models import Utilizador
import schemas
from dependencies import pegar_sessao, verificar_token
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["sign-up", "login", "sign-up-admin"])

def criar_token(id_utilizador, duracao=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) ):
    dict_info = {
        "sub": str(id_utilizador),
        "exp": datetime.now(timezone.utc) + duracao
    }
    token = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return token

def autenticar_utilizador(email, senha, session):
    utilizador = session.query(Utilizador).filter(Utilizador.email == email).first()
    if not utilizador or not bcrypt_context.verify(senha, utilizador.senha):
        return False
    return utilizador

@auth_router.post("/sign-up")
async def sign_up(utilizador_schema: schemas.UtilizadorSchema, session: Session = Depends(pegar_sessao)):
    utilizador = session.query(Utilizador).filter(Utilizador.email == utilizador_schema.email).first()
    if utilizador:
        raise HTTPException(status_code=400, detail="USER ALREADY EXISTIS")
    senha_hash = bcrypt_context.hash(utilizador_schema.senha)
    novo_utilizador = Utilizador(utilizador_schema.nome, utilizador_schema.email, senha_hash)
    session.add(novo_utilizador)
    session.commit()
    return {
        "mensagem": f"Utilizador cadastrado! Bemvindo {utilizador_schema.nome}!"
    }

@auth_router.post("/login")
async def login(login_schema: schemas.LoginSchema, session: Session = Depends(pegar_sessao)):
    utilizador = autenticar_utilizador(login_schema.email, login_schema.senha, session)
    if not utilizador:
        raise HTTPException(status_code=401, detail="INVALID CREDENTIALS")
    access_token = criar_token(utilizador.id)
    refresh_token = criar_token(utilizador.id, duracao=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    utilizador = autenticar_utilizador(dados_formulario.username, dados_formulario.password, session)
    if not utilizador:
        raise HTTPException(status_code=401, detail="INVALID CREDENTIAL")
    access_token = criar_token(utilizador.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
    
@auth_router.post("/sign-up-admin")
async def sign_up_admin(utilizador_schema: schemas.UtilizadorSchema, utilizador: Utilizador = Depends(verificar_token), session: Session = Depends(pegar_sessao)):
    if not utilizador.admin:
        raise HTTPException(status_code=403, detail="JUST FOR ADMINS")
    utilizador_exist = session.query(Utilizador).filter(Utilizador.email == utilizador_schema.email).first()
    if utilizador_exist:
        raise HTTPException(status_code=401, detail="USER ALREADY EXISTS")
    senha_hash = bcrypt_context.hash(utilizador_schema.senha)
    novo_utilizador = Utilizador(utilizador_schema.nome, utilizador_schema.email, senha_hash, admin=True)
    session.add(novo_utilizador)
    session.commit()
    return {
        "mensagem": f"Utilizador admin cadastrado com sucesso! Bemvindo {utilizador_schema.nome}"
    }


@auth_router.get("/refresh")
async def refresh_token(utilizador: Utilizador = Depends(verificar_token)):
    access_token = criar_token(utilizador.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
