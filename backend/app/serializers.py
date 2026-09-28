def serialize_servidor(row: dict) -> dict:
    return {
        "id": row["id"],
        "id_portal": row["id_portal"],
        "nome": row["nome"],
        "cpf_mascarado": row["cpf_mascarado"],
        "matricula": row["matricula"],
        "uf": row["uf"],
        "situacao": row["situacao"],
        "tipo_aposentadoria": row["tipo_aposentadoria"],
        "data_aposentadoria": row["data_aposentadoria"].isoformat()
        if row["data_aposentadoria"]
        else None,
        "regime_juridico": row["regime_juridico"],
        "jornada": row["jornada"],
        "cargo": {
            "id": row["cargo_id"],
            "descricao": row["cargo"],
            "classe": row["cargo_classe"],
            "carreira": row["carreira"],
        },
        "orgao": {
            "id": row["orgao_id"],
            "nome": row["orgao"],
            "sigla": row["orgao_sigla"],
            "uf_sede": row["uf_sede"],
            "orgao_superior": row["orgao_superior"],
        },
    }


def serialize_cargo(row: dict) -> dict:
    return {
        "id": row["id"],
        "descricao": row["descricao"],
        "classe": row["classe"],
        "carreira": row["carreira"],
        "jornada": row["jornada"],
    }


def serialize_orgao(row: dict) -> dict:
    return {
        "id": row["id"],
        "codigo": row["codigo"],
        "nome": row["nome"],
        "sigla": row["sigla"],
        "uf_sede": row["uf_sede"],
        "orgao_superior": row["orgao_superior"],
    }
