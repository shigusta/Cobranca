from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud, db
from app.whatsapp import enviar_mensagem

router = APIRouter()



# --------- Clientes ----------
@router.post("/clientes/", response_model=schemas.ClienteResponse)
def criar_cliente(cliente: schemas.ClienteCreate, database: Session = Depends(db.get_db)):
    return crud.criar_cliente(database, cliente)

@router.get("/clientes/", response_model=List[schemas.ClienteResponse])
def listar_clientes(database: Session = Depends(db.get_db)):
    return crud.listar_clientes(database)

# --------- Cobranças ----------
@router.post("/enviar")
async def enviar_cobranca(dados: dict):
    numero = dados["telefone"]
    mensagem = dados["mensagem"] 
    enviar_mensagem(numero, mensagem)
    return {"status": "ok", "destino": numero}

@router.post("/cobrancas/", response_model=schemas.CobrancaResponse)
def criar_cobranca(cobranca: schemas.CobrancaCreate, database: Session = Depends(db.get_db)):
    return crud.criar_cobranca(database, cobranca)

@router.get("/cobrancas/", response_model=List[schemas.CobrancaResponse])
def listar_cobrancas(database: Session = Depends(db.get_db)):
    return crud.listar_cobrancas(database)

@router.post("/cobrancas/{cobranca_id}/reenviar", response_model=schemas.CobrancaResponse)
def reenviar_cobranca(cobranca_id: int, database: Session = Depends(db.get_db)):
    c = crud.reenviar_cobranca(database, cobranca_id)
    if not c:
        raise HTTPException(status_code=404, detail="Cobrança não encontrada")
    return c

@router.post("/cobrancas/{cobranca_id}/status", response_model=schemas.CobrancaResponse)
def atualizar_status(cobranca_id: int, payload: schemas.CobrancaStatusUpdate, database: Session = Depends(db.get_db)):
    c = crud.atualizar_status_cobranca(database, cobranca_id, payload.status)
    if not c:
        raise HTTPException(status_code=404, detail="Cobrança não encontrada")
    return c
