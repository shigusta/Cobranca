import datetime
import pywhatkit as kit
from app.db import SessionLocal
from app import models


def enviar_mensagem(numero: str, mensagem: str):
    try:
        agora = datetime.datetime.now()
        hora = agora.hour
        minuto = agora.minute + 1  # sempre agenda 1 minuto adiante

        kit.sendwhatmsg(numero, mensagem, hora, minuto, wait_time=10, tab_close=True)
        print(f"✅ Mensagem agendada para {numero}: {mensagem[:30]}...")
    except Exception as e:
        print(f"❌ Erro ao enviar mensagem para {numero}: {e}")


def enviar_para_todos_clientes():
    """Busca todos os clientes no banco e envia mensagem para cada um"""
    db = SessionLocal()
    clientes = db.query(models.Cliente).all()

    if not clientes:
        print("⚠ Nenhum cliente encontrado no banco")
        return

    for i, cliente in enumerate(clientes, start=1):
        mensagem = f"Olá {cliente.nome}, esta é uma mensagem de teste do sistema de cobrança 🚀"
        
        agora = datetime.datetime.now()
        hora = agora.hour
        minuto = agora.minute + i  # agenda cada mensagem 1 min depois da outra

        try:
            kit.sendwhatmsg(cliente.telefone, mensagem, hora, minuto, wait_time=10, tab_close=True)
            print(f"✅ Mensagem agendada para {cliente.nome} ({cliente.telefone}) às {hora}:{minuto:02d}")
        except Exception as e:
            print(f"❌ Erro ao agendar mensagem para {cliente.nome} ({cliente.telefone}): {e}")


if __name__ == "__main__":
    enviar_para_todos_clientes()
