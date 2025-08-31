# app/services/mensagens.py
import pywhatkit as kit
import datetime
import time
import traceback

def enviar_mensagem(telefone: str, mensagem: str, modo_instantaneo: bool = True, wait_time: int = 20):
    """
    Tenta enviar uma mensagem via WhatsApp Web.
    - telefone: formato +55...
    - mensagem: texto simples
    - modo_instantaneo: se True usa sendwhatmsg_instantly (envio imediato),
      se False usa sendwhatmsg (agendado 1 minuto no futuro)
    - wait_time: tempo de espera usado pelo pywhatkit (segundos)
    Retorna dict com {ok: bool, detalhe: str}
    """
    try:
        if not telefone or not mensagem:
            return {"ok": False, "detalhe": "telefone ou mensagem vazios"}

        agora = datetime.datetime.now()

        if modo_instantaneo:
            # tentativa "instantânea"
            # sendwhatmsg_instantly internamente usa pyautogui e pode falhar se
            # o navegador estiver com comportamento diferente; testamos com wait_time maior
            kit.sendwhatmsg_instantly(
                phone_no=telefone,
                message=mensagem,
                wait_time=wait_time,
                tab_close=False,   # mantenha aberto para debug; depois pode mudar
                close_time=3
            )
            # dar um pequeno sleep para garantir que o pyautogui executou ações
            time.sleep(2)
            return {"ok": True, "detalhe": "agendado/iniciado (instantâneo)"}
        else:
            # agenda um minuto à frente — pywhatkit exige agendamento
            hora = agora.hour
            minuto = (agora.minute + 1) % 60
            kit.sendwhatmsg(telefone, mensagem, hora, minuto, wait_time=wait_time, tab_close=False)
            return {"ok": True, "detalhe": f"agendado para {hora}:{minuto:02d}"}

    except Exception as e:
        tb = traceback.format_exc()
        return {"ok": False, "detalhe": f"{e}", "trace": tb}
