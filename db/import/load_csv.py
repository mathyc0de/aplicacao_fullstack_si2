#!/usr/bin/env python3
"""Carrega os CSVs de aposentados e carreiras do dados.gov.br no PostgreSQL."""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from datetime import date
from pathlib import Path
from typing import Iterator

ENCODING = "latin-1"
DELIMITER = ";"

APOSENTADOS_COLS = [
    "nome", "cpf", "matricula", "orgao", "sigla_orgao", "orgao_vinculacao",
    "cargo", "classe", "padrao", "referencia", "nivel", "tipo_aposentadoria",
    "fund_legal", "portaria", "dt_inatividade", "nome_ocorrencia",
    "dt_ingresso", "valor",
]
CARREIRAS_COLS = [
    "nome", "cpf", "codigo_carreira", "cargo", "uf_upag", "orgao",
    "mes_referencia", "valor",
]

UF_RE = re.compile(r"^[A-Z]{2}$")
BATCH_LOG = 100_000


def clean(value: str, max_len: int | None = None) -> str:
    value = re.sub(r"\s+", " ", (value or "").replace("\x00", " ")).strip()
    return value[:max_len] if max_len else value


def parse_ddmmaaaa(value: str) -> date | None:
    value = clean(value)
    if len(value) != 8 or not value.isdigit():
        return None
    try:
        return date(int(value[4:]), int(value[2:4]), int(value[:2]))
    except ValueError:
        return None


def read_rows(path: Path, columns: list[str]) -> Iterator[dict[str, str]]:
    with path.open("r", encoding=ENCODING, newline="") as handle:
        reader = csv.reader(handle, delimiter=DELIMITER, quoting=csv.QUOTE_NONE)
        first = True
        for fields in reader:
            if first:
                first = False
                if fields and clean(fields[0]).lower() == "nome":
                    continue
            if len(fields) < len(columns):
                yield {}
                continue
            yield dict(zip(columns, fields))


def aposentado_tuple(row: dict[str, str]):
    nome = clean(row.get("nome", ""), 200)
    if len(nome) < 2:
        return None
    return (
        nome,
        clean(row["cpf"], 14) or None,
        clean(row["matricula"], 20) or None,
        clean(row["orgao"], 200) or "NAO INFORMADO",
        clean(row["sigla_orgao"], 30) or None,
        clean(row["orgao_vinculacao"], 20) or None,
        clean(row["cargo"], 200) or "NAO INFORMADO",
        clean(row["classe"], 10) or None,
        clean(row["tipo_aposentadoria"], 80) or None,
        parse_ddmmaaaa(row["dt_inatividade"]),
    )


def carreira_tuple(row: dict[str, str]):
    nome = clean(row.get("nome", ""), 200)
    if len(nome) < 2:
        return None
    uf = clean(row["uf_upag"]).upper()
    return (
        nome,
        clean(row["cpf"], 14) or None,
        clean(row["codigo_carreira"], 200) or None,
        clean(row["cargo"], 200) or "NAO INFORMADO",
        uf if UF_RE.match(uf) else None,
        clean(row["orgao"], 200) or "NAO INFORMADO",
    )


def check_file(label: str, path: Path, columns: list[str], to_tuple, limit: int | None) -> int:
    ok = bad = 0
    sample = None
    for row in read_rows(path, columns):
        data = to_tuple(row) if row else None
        if data is None:
            bad += 1
            continue
        ok += 1
        sample = sample or data
        if limit and ok >= limit:
            break
    print(f"{label}: {ok} linhas válidas, {bad} descartadas")
    print(f"  exemplo: {sample}")
    return ok


def copy_into(cursor, table: str, columns: list[str], rows: Iterator[tuple], label: str) -> int:
    count = 0
    with cursor.copy(f"COPY {table} ({', '.join(columns)}) FROM STDIN") as copy:
        for data in rows:
            copy.write_row(data)
            count += 1
            if count % BATCH_LOG == 0:
                print(f"  {label}: {count} lidos...", flush=True)
    return count


def valid(rows: Iterator[dict[str, str]], to_tuple) -> Iterator[tuple]:
    for row in rows:
        data = to_tuple(row) if row else None
        if data is not None:
            yield data


def load_aposentados(cursor, path: Path, limit: int | None) -> int:
    cursor.execute(
        """
        CREATE TEMP TABLE stg_aposentados (
            nome text, cpf text, matricula text, orgao text, sigla text,
            orgao_sup text, cargo text, classe text, tipo text, dt date
        ) ON COMMIT DROP
        """
    )
    rows = valid(read_rows(path, APOSENTADOS_COLS), aposentado_tuple)
    if limit:
        rows = (r for _, r in zip(range(limit), rows))
    total = copy_into(
        cursor, "stg_aposentados",
        ["nome", "cpf", "matricula", "orgao", "sigla", "orgao_sup", "cargo", "classe", "tipo", "dt"],
        rows, "aposentados",
    )

    cursor.execute(
        """
        INSERT INTO cargos (descricao, classe)
        SELECT DISTINCT ON (upper(cargo)) cargo, classe FROM stg_aposentados
        ON CONFLICT (upper(descricao)) DO NOTHING
        """
    )
    cursor.execute(
        """
        INSERT INTO orgaos (nome, sigla, uf_sede, orgao_superior)
        SELECT DISTINCT ON (upper(s.orgao)) s.orgao, s.sigla, 'DF', s.orgao_sup
        FROM stg_aposentados s
        WHERE NOT EXISTS (SELECT 1 FROM orgaos o WHERE upper(o.nome) = upper(s.orgao))
        """
    )
    cursor.execute(
        """
        INSERT INTO servidores (
            nome, cpf_mascarado, matricula, cargo_id, orgao_id, uf, situacao,
            tipo_aposentadoria, data_aposentadoria, regime_juridico
        )
        SELECT s.nome, s.cpf, s.matricula, c.id, o.id, o.uf_sede, 'APOSENTADO',
               s.tipo, s.dt, 'Regime Jurídico Único'
        FROM stg_aposentados s
        JOIN (SELECT upper(descricao) AS k, min(id) AS id FROM cargos GROUP BY 1) c
             ON c.k = upper(s.cargo)
        JOIN (SELECT DISTINCT ON (upper(nome)) upper(nome) AS k, id, uf_sede
              FROM orgaos ORDER BY upper(nome), id) o
             ON o.k = upper(s.orgao)
        """
    )
    return total


def load_carreiras(cursor, path: Path, limit: int | None) -> int:
    cursor.execute(
        """
        CREATE TEMP TABLE stg_carreiras (
            nome text, cpf text, carreira text, cargo text, uf text, orgao text
        ) ON COMMIT DROP
        """
    )
    rows = valid(read_rows(path, CARREIRAS_COLS), carreira_tuple)
    if limit:
        rows = (r for _, r in zip(range(limit), rows))
    total = copy_into(
        cursor, "stg_carreiras",
        ["nome", "cpf", "carreira", "cargo", "uf", "orgao"],
        rows, "carreiras",
    )

    cursor.execute(
        """
        INSERT INTO cargos (descricao, carreira)
        SELECT DISTINCT ON (upper(cargo)) cargo, carreira FROM stg_carreiras
        ON CONFLICT (upper(descricao)) DO NOTHING
        """
    )
    cursor.execute(
        """
        INSERT INTO orgaos (nome, uf_sede)
        SELECT s.orgao, COALESCE(mode() WITHIN GROUP (ORDER BY s.uf), 'DF')
        FROM stg_carreiras s
        WHERE NOT EXISTS (SELECT 1 FROM orgaos o WHERE upper(o.nome) = upper(s.orgao))
        GROUP BY s.orgao
        """
    )
    cursor.execute(
        """
        INSERT INTO servidores (nome, cpf_mascarado, cargo_id, orgao_id, uf, situacao)
        SELECT s.nome, s.cpf, c.id, o.id, COALESCE(s.uf, o.uf_sede), 'ATIVO'
        FROM stg_carreiras s
        JOIN (SELECT upper(descricao) AS k, min(id) AS id FROM cargos GROUP BY 1) c
             ON c.k = upper(s.cargo)
        JOIN (SELECT DISTINCT ON (upper(nome)) upper(nome) AS k, id, uf_sede
              FROM orgaos ORDER BY upper(nome), id) o
             ON o.k = upper(s.orgao)
        """
    )
    return total


def run_load(args) -> int:
    import psycopg

    if not args.database_url:
        print("informe --database-url ou DATABASE_URL", file=sys.stderr)
        return 2

    with psycopg.connect(args.database_url) as conn:
        with conn.cursor() as cursor:
            if args.replace:
                cursor.execute("TRUNCATE servidores RESTART IDENTITY")
                print("servidores existentes removidos (--replace)")
            total = 0
            if args.aposentados:
                n = load_aposentados(cursor, args.aposentados, args.limit)
                print(f"aposentados: {n} registros")
                total += n
            if args.carreiras:
                n = load_carreiras(cursor, args.carreiras, args.limit)
                print(f"carreiras (ativos): {n} registros")
                total += n
            if args.replace:
                cursor.execute(
                    "DELETE FROM cargos c WHERE NOT EXISTS (SELECT 1 FROM servidores s WHERE s.cargo_id = c.id)"
                )
                cursor.execute(
                    "DELETE FROM orgaos o WHERE NOT EXISTS (SELECT 1 FROM servidores s WHERE s.orgao_id = o.id)"
                )
            if args.dry_run:
                conn.rollback()
                print(f"dry-run: {total} registros seriam importados (nada gravado)")
            else:
                conn.commit()
                cursor.execute("ANALYZE servidores")
                conn.commit()
                cursor.execute("SELECT situacao, count(*) FROM servidores GROUP BY 1 ORDER BY 1")
                for situacao, qtd in cursor.fetchall():
                    print(f"  {situacao}: {qtd}")
                print(f"total importado: {total}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Importa CSVs do dados.gov.br")
    parser.add_argument("--aposentados", type=Path, help="APOSENTADOS_*.csv")
    parser.add_argument("--carreiras", type=Path, help="CARREIRA_*.txt")
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL"))
    parser.add_argument("--limit", type=int, help="máximo de linhas por arquivo")
    parser.add_argument("--replace", action="store_true",
                        help="apaga os servidores existentes (dados de exemplo) antes de importar")
    parser.add_argument("--dry-run", action="store_true", help="carrega e faz rollback")
    parser.add_argument("--check", action="store_true",
                        help="só lê e valida os arquivos, sem conectar ao banco")
    args = parser.parse_args()

    if not args.aposentados and not args.carreiras:
        print("informe --aposentados e/ou --carreiras", file=sys.stderr)
        return 2
    for path in (args.aposentados, args.carreiras):
        if path and not path.is_file():
            print(f"arquivo não encontrado: {path}", file=sys.stderr)
            return 2

    if args.check:
        if args.aposentados:
            check_file("aposentados", args.aposentados, APOSENTADOS_COLS, aposentado_tuple, args.limit)
        if args.carreiras:
            check_file("carreiras", args.carreiras, CARREIRAS_COLS, carreira_tuple, args.limit)
        return 0

    return run_load(args)


if __name__ == "__main__":
    raise SystemExit(main())
