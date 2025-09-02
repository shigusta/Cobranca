import argparse
import pandas as pd
from sqlalchemy import select
from .db import SessionLocal, Cliente, init_db
from .utils import normalize_br_phone

def guess_column(df, contains: str):
    for col in df.columns:
        if contains.lower() in str(col).lower():
            return col
    return None

def run(file: str, col_name: str | None, col_phone: str | None, col_status: str | None, overwrite: bool):
    init_db()
    df = pd.read_excel(file)

    col_name = col_name or guess_column(df, "TITULAR") or guess_column(df, "NOME")
    if not col_name:
        raise SystemExit("Não encontrei coluna de NOME. Use --col-name")

    if not col_phone:
        candidates = [c for c in df.columns if "TELEFONE" in str(c).upper()]
        col_phone = candidates[0] if candidates else None
    if not col_phone:
        raise SystemExit("Não encontrei coluna de TELEFONE. Use --col-phone")

    if not col_status:
        col_status = guess_column(df, "OBS") or guess_column(df, "STATUS")

    session = SessionLocal()
    inserted, updated, invalid = 0, 0, 0

    for _, row in df.iterrows():
        nome = str(row.get(col_name, "")).strip()
        telefone_raw = row.get(col_phone, "")
        telefone = normalize_br_phone(str(telefone_raw))
        if not telefone:
            invalid += 1
            continue

        status = str(row.get(col_status, "")).strip() if col_status else "aguardando"

        existing = session.execute(select(Cliente).where(Cliente.phone == telefone)).scalar_one_or_none()
        if existing:
            if overwrite:
                existing.name = nome or existing.name
                existing.status = status or existing.status
                updated += 1
            continue
        else:
            c = Cliente(name=nome or "Sem nome", phone=telefone, status=status)
            session.add(c)
            inserted += 1

    session.commit()
    session.close()
    print(f"Importação concluída. Inseridos: {inserted} | Atualizados: {updated} | Telefones inválidos: {invalid}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Importa planilha Excel para o banco (clientes).")
    parser.add_argument("--file", required=True, help="Caminho do arquivo .xlsx")
    parser.add_argument("--col-name", help="Nome da coluna de nome (ex.: TITULAR)")
    parser.add_argument("--col-phone", help="Nome da coluna de telefone (ex.: TELEFONE)")
    parser.add_argument("--col-status", help="Nome da coluna de status/obs")
    parser.add_argument("--overwrite", action="store_true", help="Sobrescreve registros existentes")
    args = parser.parse_args()
    run(args.file, args.col_name, args.col_phone, args.col_status, args.overwrite)
