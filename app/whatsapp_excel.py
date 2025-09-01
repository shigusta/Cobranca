# app/whatsapp_excel.py
import argparse
import time
from datetime import datetime
from pathlib import Path
import pandas as pd
import pywhatkit as kit

MENSAGEM_PADRAO = (
    "Oi! Esperamos que esteja tudo bem com você.\n"
    "Passando aqui só para lembrar que a sua fatura referente ao mês de *Maio* ainda está em aberto. Você pode\n"
    "acessá-la pelo nosso app, site ou pelo e-mail que enviamos.\n"
    "Se o pagamento já foi feito, por favor, desconsidere este aviso. E, se precisar de qualquer ajuda para regularizar a\n"
    "situação, conte com a gente! Estamos por aqui para o que for preciso.\n"
    "Com carinho, Kamila\n"
    "Equipe Financeiro – Kayrós Link"
)

def primeiro_nome(nome: str) -> str:
    return str(nome).strip().split()[0].title() if nome else ""

def normalizar_telefone(tel: str) -> str:
    dig = "".join(ch for ch in str(tel) if ch.isdigit())
    if dig.startswith("55"):
        return f"+{dig}"
    return f"+55{dig}"

def carregar_planilha(caminho: str) -> pd.DataFrame:
    df = pd.read_excel(caminho)
    df.columns = [c.strip().upper() for c in df.columns]
    if "NOME" not in df.columns or "TELEFONE" not in df.columns:
        raise ValueError("A planilha precisa ter as colunas: NOME e TELEFONE")
    for col in ["RESPONDEU", "TENTATIVAS", "ULTIMO_ENVIO", "ERRO_ULTIMO_ENVIO"]:
        if col not in df.columns:
            df[col] = "" if col in ["RESPONDEU", "ERRO_ULTIMO_ENVIO"] else 0
    df["TELEFONE"] = df["TELEFONE"].apply(normalizar_telefone)
    return df

def enviar_mensagem_instantanea(numero: str, texto: str, wait_time: int = 25):
    kit.sendwhatmsg_instantly(
        phone_no=numero,
        message=texto,
        wait_time=wait_time,
        tab_close=True,
        close_time=3
    )

def enviar_para_nao_respondidos(df: pd.DataFrame, delay: int, msg_padrao: str):
    filtro = ~df["RESPONDEU"].astype(str).str.lower().isin(["sim", "s", "y", "yes"])
    pendentes = df[filtro].copy()
    if pendentes.empty:
        print("✔ Não há pendentes para envio.")
        return df
    print(f"👟 Enviando para {len(pendentes)} contato(s) não respondidos...")
    for offset, (idx, row) in enumerate(pendentes.iterrows(), start=1):
        nome = str(row["NOME"]).strip()
        numero = str(row["TELEFONE"]).strip()
        texto = f"Oi {primeiro_nome(nome)},\n\n{msg_padrao}"
        print(f"📲 Enviando para {nome} - {numero}")
        try:
            enviar_mensagem_instantanea(numero, texto, wait_time=25)
            time.sleep(delay)
            tent = int(df.at[idx, "TENTATIVAS"]) if str(df.at[idx, "TENTATIVAS"]).isdigit() else 0
            df.at[idx, "TENTATIVAS"] = tent + 1
            df.at[idx, "ULTIMO_ENVIO"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df.at[idx, "ERRO_ULTIMO_ENVIO"] = ""
            print(f"✅ Enviado para {nome}")
        except Exception as e:
            df.at[idx, "ERRO_ULTIMO_ENVIO"] = str(e)
            df.at[idx, "ULTIMO_ENVIO"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"❌ Falha com {nome}: {e}")
    return df

def salvar_relatorios(df: pd.DataFrame, saida_dir: str):
    Path(saida_dir).mkdir(parents=True, exist_ok=True)
    andamento = Path(saida_dir) / "contatos_em_andamento.xlsx"
    df.to_excel(andamento, index=False)
    nao_resp = df[~df["RESPONDEU"].astype(str).str.lower().isin(["sim", "s", "y", "yes"])]
    para_ligar = Path(saida_dir) / "nao_respondidos_para_ligar.xlsx"
    nao_resp[["NOME", "TELEFONE"]].to_excel(para_ligar, index=False)
    print(f"\n🗂 Arquivos salvos: {andamento}, {para_ligar}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--arquivo", default="data/contatos_teste.xlsx")
    parser.add_argument("--saida", default="data/saida")
    parser.add_argument("--delay", type=int, default=15)
    parser.add_argument("--mensagem", default=None)
    args = parser.parse_args()
    msg = args.mensagem or MENSAGEM_PADRAO
    df = carregar_planilha(args.arquivo)
    df = enviar_para_nao_respondidos(df, delay=args.delay, msg_padrao=msg)
    salvar_relatorios(df, args.saida)

if __name__ == "__main__":
    main()
