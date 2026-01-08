from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from database import db
from main import oath2_schema, SECRET_KEY, ALGORITHM
from models import Utilizador

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oath2_schema), session: Session = Depends(pegar_sessao)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_utilizador = int(dict_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=400, detail="INVALID TOKEN")
    
    utilizador = session.query(Utilizador).filter(Utilizador.id == id_utilizador).first()
    if not utilizador:
        raise HTTPException(status_code=404 ,detail="USER NOT FOUND")
    return utilizador
