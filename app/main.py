# app/main.py
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from typing import Optional

# importar funções do whatsapp_excel
from app.whatsapp_excel import carregar_planilha, enviar_para_nao_respondidos, salvar_relatorios, MENSAGEM_PADRAO

app = FastAPI(title="Cobrancas Bot")

# CORS (dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def process_uploaded_file(path: str, delay: int = 15, mensagem: Optional[str] = None):
    try:
        print("Processando planilha:", path)
        df = carregar_planilha(path)
        df = enviar_para_nao_respondidos(df, delay=delay, msg_padrao=(mensagem or MENSAGEM_PADRAO))
        salvar_relatorios(df, str(Path(path).parent / "saida"))
        print("Processamento concluído para:", path)
    except Exception as e:
        print("Erro processando planilha:", e)

@app.post("/upload")
async def upload_planilha(background_tasks: BackgroundTasks, file: UploadFile = File(...), delay: int = 15, mensagem: Optional[str] = None):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Envie um arquivo .xlsx ou .xls")
    destino = DATA_DIR / file.filename
    with destino.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    background_tasks.add_task(process_uploaded_file, str(destino), delay, mensagem)
    return {"ok": True, "filename": str(destino)}
@app.get("/")
def home():
    return {"message": "🚀 API de Cobranças rodando! Acesse /docs para testar."}
