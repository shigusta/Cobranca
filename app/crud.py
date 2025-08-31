from sqlalchemy.orm import Session
from . import models, schemas
from app.services.mensagens import enviar_mensagem
import logging
import datetime

logger = logging.getLogger("cobrancas")

# -------------------
# Cliente
# -------------------
def criar_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(nome=cliente.nome, telefone=cliente.telefone)
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def listar_clientes(db: Session):
    return db.query(models.Cliente).all()

# -------------------
# Cobranca
# -------------------
def criar_cobranca(db: Session, cobranca: schemas.CobrancaCreate):
    db_cobranca = models.Cobranca(
        valor=cobranca.valor,
        vencimento=cobranca.vencimento,
        status=cobranca.status or "pendente",
        cliente_id=cobranca.cliente_id,
    )
    db.add(db_cobranca)
    db.commit()
    db.refresh(db_cobranca)

    cliente = db.query(models.Cliente).get(db_cobranca.cliente_id)
    if cliente and cliente.telefone:
        mensagem = f"Olá {cliente.nome}, você tem uma cobrança de R$ {db_cobranca.valor:.2f} com vencimento em {db_cobranca.vencimento}."
        resultado = enviar_mensagem(cliente.telefone, mensagem, modo_instantaneo=True, wait_time=30)
        logger.info("Envio mensagem: %s", resultado)
        # opcional: gravar resultado em campo de log no DB (ou MessageLog)
        if resultado.get("ok"):
            db_cobranca.ultimo_envio = datetime.datetime.now()
            db_cobranca.tentativas = (db_cobranca.tentativas or 0) + 1
            db.commit()
            db.refresh(db_cobranca)
        else:
            logger.error("Falha envio: %s", resultado)
    return db_cobranca

def listar_cobrancas(db: Session):
    return db.query(models.Cobranca).all()

def reenviar_cobranca(db: Session, cobranca_id: int):
    cobranca = db.query(models.Cobranca).get(cobranca_id)
    if not cobranca:
        return None
    cliente = db.query(models.Cliente).get(cobranca.cliente_id)
    if cliente:
        mensagem = f"Olá {cliente.nome}, você tem uma cobrança de R$ {cobranca.valor} com vencimento em {cobranca.vencimento}."
        enviar_mensagem(cliente.telefone, mensagem)
    return cobranca

def atualizar_status_cobranca(db: Session, cobranca_id: int, status: str):
    cobranca = db.query(models.Cobranca).get(cobranca_id)
    if not cobranca:
        return None
    cobranca.status = status
    db.commit()
    db.refresh(cobranca)
    
    # pega o cliente
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cobranca.cliente_id).first()

    if cliente and cliente.telefone:
        enviar_mensagem(cliente.telefone, status)

    return cobranca