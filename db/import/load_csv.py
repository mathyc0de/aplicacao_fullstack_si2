#!/usr/bin/env python3
"""Carrega CSVs oficiais do dados.gov.br no PostgreSQL.

O script espera colunas compatíveis com o cadastro de aposentados e com a
tabela de carreiras/cargos. Use --dry-run para validar o arquivo sem gravar.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

import psycopg


def open_csv(path: Path):
    with path.open("r", encoding="latin-1", newline="") as handle:
        sample = handle.read(4096)
        handle.seek(0)
        delimiter = ";" if sample.count(";") >= sample.count(",") else ","
        reader = csv.DictReader(handle, delimiter=delimiter)
        for row in reader:
            yield {key.strip().upper(): (value or "").strip() for key, value in row.items()}


def upsert_orgao(cursor, nome: str, sigla: str, uf: str) -> int:
    cursor.execute(
        """
        INSERT INTO orgaos (nome, sigla, uf_sede)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING id
        """,
        (nome, sigla or None, uf or "DF"),
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("SELECT id FROM orgaos WHERE nome = %s", (nome,))
    found = cursor.fetchone()
    return found[0] if found else None


def upsert_cargo(cursor, descricao: str, classe: str, carreira: str) -> int:
    cursor.execute(
        """
        INSERT INTO cargos (descricao, classe, carreira)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING id
        """,
        (descricao, classe or None, carreira or None),
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("SELECT id FROM cargos WHERE descricao = %s", (descricao,))
    found = cursor.fetchone()
    return found[0]


def load_aposentados(conn, path: Path, limit: int | None) -> int:
    count = 0
    with conn.cursor() as cursor:
        for row in open_csv(path):
            nome = row.get("NOME") or row.get("NOME_SERVIDOR")
            if not nome:
                continue
            cargo_nome = row.get("DESCRICAO_CARGO") or row.get("DESCRIÇÃO-CARGO-EMPREGO") or "Não informado"
            orgao_nome = row.get("ORGAO_LOTACAO") or row.get("NOME ÓRGÃO DE ORIGEM") or "Não informado"
            sigla = row.get("SIGLA ÓRGÃO DE ORIGEM") or row.get("SIGLA_ORGAO") or ""
            uf = (row.get("UF_EXERCICIO") or row.get("UF") or "DF")[:2].upper()
            cargo_id = upsert_cargo(cursor, cargo_nome, row.get("CLASSE_CARGO", ""), "")
            orgao_id = upsert_orgao(cursor, orgao_nome, sigla, uf)
            cursor.execute(
                """
                INSERT INTO servidores (
                    nome, cpf_mascarado, matricula, cargo_id, orgao_id, uf, situacao,
                    tipo_aposentadoria, regime_juridico
                ) VALUES (%s, %s, %s, %s, %s, %s, 'APOSENTADO', %s, %s)
                """,
                (
                    nome,
                    row.get("CPF") or row.get("CPF_MASCARADO"),
                    row.get("MATRICULA"),
                    cargo_id,
                    orgao_id,
                    uf,
                    row.get("TIPO_APOSENTADORIA") or row.get("DESCRIÇÃO DO TIPO DE APOSENTADORIA"),
                    row.get("REGIME_JURIDICO"),
                ),
            )
            count += 1
            if limit and count >= limit:
                break
    return count


def main() -> int:
    parser = argparse.ArgumentParser(description="Importa CSVs do dados.gov.br")
    parser.add_argument("--aposentados", type=Path)
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL"))
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.database_url:
        print("informe --database-url ou DATABASE_URL", file=sys.stderr)
        return 2
    if not args.aposentados:
        print("informe --aposentados", file=sys.stderr)
        return 2

    with psycopg.connect(args.database_url) as conn:
        loaded = load_aposentados(conn, args.aposentados, args.limit)
        if args.dry_run:
            conn.rollback()
            print(f"dry-run: {loaded} registros seriam importados")
        else:
            conn.commit()
            print(f"importados: {loaded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
# Fonte: Portal Brasileiro de Dados Abertos (dados.gov.br).
