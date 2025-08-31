from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    telefone = Column(String, nullable=False)

    cobrancas = relationship("Cobranca", back_populates="cliente")


class Cobranca(Base):
    __tablename__ = "cobrancas"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float, nullable=False)
    vencimento = Column(Date, nullable=False)
    status = Column(String, default="pendente")
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="cobrancas")
