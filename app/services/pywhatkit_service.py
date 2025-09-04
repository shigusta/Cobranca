import pywhatkit
import time

def send_whatsapp_pywhatkit(to_number: str, message: str):
    """Envia mensagem WhatsApp via PyWhatKit"""
    try:
        # Enviar imediatamente
        pywhatkit.sendwhatmsg_instantly(to_number, message, wait_time=10, tab_close=True)
        time.sleep(5) 
        return {"status": "sent"}
    except Exception as e:
        return {"error": str(e)}
