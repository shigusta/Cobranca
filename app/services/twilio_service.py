import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv(dotenv_path="data/.env")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_from = os.getenv("TWILIO_WHATSAPP_FROM")

client = Client(account_sid, auth_token)

def send_whatsapp_twilio(to_number: str, message: str):
    """Envia mensagem WhatsApp via Twilio"""
    try:
        msg = client.messages.create(
            from_=whatsapp_from,
            body=message,
            to=f"whatsapp:{to_number}"
        )
        print(f"✅ Twilio message SID: {msg.sid}, status: {msg.status}")
        return {"sid": msg.sid, "status": msg.status}
    except Exception as e:
        print(f"❌ Twilio error: {e}")
        return {"error": str(e)}
