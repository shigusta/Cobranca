import datetime
import pywhatkit as kit
from app.db import SessionLocal
from app import models


import pywhatkit as kit

def enviar_mensagem(numero: str, mensagem: str):
    try:
        print(f"📩 Enviando para {numero}: {mensagem[:30]}...")
        kit.sendwhatmsg_instantly(
            phone_no=numero,
            message=mensagem,
            wait_time=5,   # tempo para abrir o chat
            tab_close=True, # fecha a aba depois
            close_time=3    # espera antes de fechar
        )
        print(f"✅ Mensagem enviada para {numero}")
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
        minuto = agora.minute + i 

        try:
            kit.sendwhatmsg(cliente.telefone, mensagem, hora, minuto, wait_time=10, tab_close=True)
            print(f"✅ Mensagem agendada para {cliente.nome} ({cliente.telefone}) às {hora}:{minuto:02d}")
        except Exception as e:
            print(f"❌ Erro ao agendar mensagem para {cliente.nome} ({cliente.telefone}): {e}")


if __name__ == "__main__":

    enviar_para_todos_clientes()
