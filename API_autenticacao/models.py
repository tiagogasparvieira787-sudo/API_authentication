from sqlalchemy import Column, String, Integer, Boolean, DateTime
from database import Base
from datetime import datetime, timezone

class Utilizador(Base):
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String, nullable=False)
    created_at = Column("created_at", DateTime, default=lambda: datetime.now(timezone.utc))
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin
