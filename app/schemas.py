from pydantic import BaseModel
from datetime import date
from typing import Optional

# -------------------
# Cliente
# -------------------
class ClienteBase(BaseModel):
    nome: str
    telefone: str

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(BaseModel):
    id: int
    nome: str
    telefone: str
    class Config:
        from_attributes = True

# -------------------
# Cobranca
# -------------------
class CobrancaBase(BaseModel):
    valor: float
    vencimento: date
    status: Optional[str] = "pendente"

class CobrancaCreate(CobrancaBase):
    cliente_id: int

class CobrancaResponse(CobrancaBase):
    id: int
    cliente_id: int
    class Config:
        orm_mode = True

class CobrancaStatusUpdate(BaseModel):
    status: str
