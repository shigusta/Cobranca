import os
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN", "")
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "meu_token_de_verificacao")

WHATSAPP_TEMPLATE_NAME_1 = os.getenv("WHATSAPP_TEMPLATE_NAME_1", "cobranca_primeiro_aviso")
WHATSAPP_TEMPLATE_NAME_2 = os.getenv("WHATSAPP_TEMPLATE_NAME_2", "cobranca_segundo_aviso")
WHATSAPP_TEMPLATE_LANG = os.getenv("WHATSAPP_TEMPLATE_LANG", "pt_BR")

RESEND_INTERVAL_DAYS = int(os.getenv("RESEND_INTERVAL_DAYS", "2"))
MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", "5"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cobrancas.db")
PORT = int(os.getenv("PORT", "8000"))
SIMULATE_SENDING = os.getenv("SIMULATE_SENDING", "true").lower() == "true"
