# app/main.py
from fastapi import FastAPI, File, UploadFile, BackgroundTasks, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil
from typing import Optional

from .whatsapp_excel import (
    carregar_planilha,
    enviar_para_nao_respondidos,
    salvar_relatorios,
    set_execucao,
    status_execucao,
)
from app import routes

app = FastAPI(title="Cobrancas Bot")

# Incluir o router do WhatsApp
app.include_router(routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def _processar_planilha(path: str, delay: int, mensagem: str):
    try:
        print(">>> Iniciando processamento da planilha")
        print("Mensagem recebida:", mensagem)
        print("Arquivo:", path)

        df = carregar_planilha(path)
        print("Planilha carregada:", df.head())

        df = enviar_para_nao_respondidos(df, delay=delay, msg_padrao=mensagem)
        print("Envios realizados")

        salvar_relatorios(df, str(Path(path).parent / "saida"))
        print("Relatórios salvos em:", Path(path).parent / "saida")

        print("Concluído:", path)
    except Exception as e:
        print("Erro processando planilha:", e)


@app.post("/upload")
async def upload_planilha(
    file: UploadFile = File(...),
    delay: int = Form(15),
    mensagem: str = Form(...),
):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Envie um arquivo .xlsx ou .xls")

    destino = DATA_DIR / file.filename
    with destino.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🔥 Executa direto (sem background) para testar
    _processar_planilha(str(destino), int(delay), mensagem)

    return {"ok": True, "filename": str(destino)}

@app.post("/parar")
def parar_envio():
    set_execucao(False)
    return {"ok": True}

@app.get("/status")
def status():
    return status_execucao()