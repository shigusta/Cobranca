from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    telefone = Column(String, unique=True, index=True, nullable=False)  # formato internacional, ex: +5511999999999
    email = Column(String, unique=True, index=True, nullable=True)

    cobrancas = relationship("Cobranca", back_populates="cliente", cascade="all, delete-orphan")


class Cobranca(Base):
    __tablename__ = "cobrancas"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    vencimento = Column(Date, nullable=False)
    status = Column(String, default="pendente", index=True)   # pendente | respondido | pago | cancelado
    ultimo_envio = Column(DateTime, nullable=True)
    tentativas = Column(Integer, default=0)
    max_tentativas = Column(Integer, default=5)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="cobrancas")