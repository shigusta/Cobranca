import os
from dotenv import load_dotenv
from twilio.rest import Client

# Carregar variáveis do .env
load_dotenv(dotenv_path="data/.env")

print("SID:", repr(os.getenv("TWILIO_ACCOUNT_SID")))
print("TOKEN:", repr(os.getenv("TWILIO_AUTH_TOKEN")))

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp = os.getenv("TWILIO_WHATSAPP_FROM")

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_=from_whatsapp,
    to="whatsapp:+556194121708",  # Seu número no formato correto
    body="⚡ Teste de envio via Twilio + Python"
)

print(message.sid)
