import argparse
from datetime import datetime
from pathlib import Path
import time
import pandas as pd
import pywhatkit as kit

# Flag global para interromper o loop
_EXECUTANDO = False

def set_execucao(rodando: bool):
    global _EXECUTANDO
    _EXECUTANDO = rodando

def status_execucao():
    return {"executando": _EXECUTANDO}

def carregar_planilha(caminho: str) -> pd.DataFrame:
    df = pd.read_excel(caminho)
    cols_lower = {c.lower(): c for c in df.columns}

    # Aceita TITULAR/NOME e TELEFONE/NUMERO
    nome_col = cols_lower.get("nome") or cols_lower.get("titular")
    numero_col = cols_lower.get("numero") or cols_lower.get("telefone")

    if not nome_col or not numero_col:
        raise ValueError("A planilha precisa ter as colunas NOME/TITULAR e NUMERO/TELEFONE.")

    df = df.rename(columns={
        nome_col: "NOME",
        numero_col: "NUMERO",
    })

    if "STATUS" not in df.columns:
        df["STATUS"] = "nao_enviado"

    return df

def _normaliza_numero(numero: str) -> str:
    numero = str(numero).strip()
    if not numero.startswith("+"):
        # Adiciona +55 se não tiver DDI (Brasil)
        numero = "+55" + numero
    return numero

def enviar_mensagem_instantanea(numero: str, texto: str, wait_time: int = 25):
    kit.sendwhatmsg_instantly(
        phone_no=numero,
        message=texto,
        wait_time=wait_time,
        tab_close=True,
        close_time=3
    )

def enviar_para_nao_respondidos(df: pd.DataFrame, delay: int, msg_padrao: str) -> pd.DataFrame:
    global _EXECUTANDO
    _EXECUTANDO = True
    try:
        for idx, row in df.iterrows():
            if not _EXECUTANDO:
                print(">>> Execução interrompida pelo usuário")
                break

            numero = _normaliza_numero(row["NUMERO"])
            nome = str(row.get("NOME", "")).strip()
            mensagem = (msg_padrao or "").replace("{nome}", nome)

            print(f"Enviando para {numero} -> {mensagem}")

            try:
                enviar_mensagem_instantanea(numero, mensagem)
                df.at[idx, "STATUS"] = "enviado"
            except Exception as e:
                df.at[idx, "STATUS"] = f"erro: {e}"

            time.sleep(int(delay))
    finally:
        _EXECUTANDO = False

    return df

def salvar_relatorios(df: pd.DataFrame, pasta_saida: str):
    out = Path(pasta_saida)
    out.mkdir(parents=True, exist_ok=True)

    enviados = df[df["STATUS"] == "enviado"]
    nao_enviados = df[df["STATUS"] != "enviado"]

    enviados.to_excel(out / "contatos_em_andamento.xlsx", index=False)
    nao_enviados.to_excel(out / "nao_respondidos_para_ligar.xlsx", index=False)

# (Opcional) Bloco principal para rodar como script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Envio de mensagens WhatsApp via planilha Excel")
    parser.add_argument("arquivo", help="Caminho da planilha Excel")
    parser.add_argument("--delay", type=int, default=15, help="Delay entre envios (segundos)")
    parser.add_argument("--mensagem", type=str, default="Olá {nome}, sua cobrança está pendente.", help="Mensagem padrão")
    parser.add_argument("--saida", type=str, default="data", help="Pasta de saída dos relatórios")
    args = parser.parse_args()

    df = carregar_planilha(args.arquivo)
    df_result = enviar_para_nao_respondidos(df, args.delay, args.mensagem)
    salvar_relatorios(df_result, args.saida)
    print("Processamento concluído.")
