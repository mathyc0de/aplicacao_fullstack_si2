from __future__ import annotations

import requests


class ServidoresClient:
    def __init__(self, base_url: str = "http://localhost:8000") -> None:
        self.base_url = base_url.rstrip("/")

    def search(self, **params) -> dict:
        response = requests.get(
            f"{self.base_url}/api/servidores",
            params={key: value for key, value in params.items() if value},
            timeout=15,
        )
        payload = response.json()
        if response.status_code >= 400:
            raise RuntimeError(payload.get("message", "Falha na consulta"))
        return payload

    def ufs(self) -> list[str]:
        response = requests.get(f"{self.base_url}/api/ufs", timeout=10)
        response.raise_for_status()
        return response.json().get("todas", [])
