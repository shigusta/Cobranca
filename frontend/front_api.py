from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import shutil
import os
import subprocess

app = FastAPI()

UPLOAD_DIR = "data"

@app.post("/upload-planilha/")
async def upload_planilha(file: UploadFile = File(...), delay: int = Form(20)):
    try:
        # Salva planilha na pasta data
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Executa o script whatsapp_excel.py
        comando = [
            "python", "-m", "app.whatsapp_excel",
            "--arquivo", file_path,
            "--saida", "data/saida",
            "--delay", str(delay)
        ]
        subprocess.Popen(comando)

        return JSONResponse({"status": "ok", "mensagem": f"Planilha {file.filename} recebida e processo iniciado"})
    except Exception as e:
        return JSONResponse({"status": "erro", "detalhes": str(e)}, status_code=500)
