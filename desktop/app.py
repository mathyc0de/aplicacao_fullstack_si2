#!/usr/bin/env python3
"""Cliente desktop da API de servidores (tkinter, fora do Docker)."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from api_client import ServidoresClient


class ConsultaApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Consulta a servidores federais")
        self.geometry("980x620")
        self.client = ServidoresClient()
        self._build()

    def _build(self) -> None:
        form = ttk.Frame(self, padding=12)
        form.pack(fill="x")

        self.nome = self._field(form, "Nome exato", 0)
        self.similar = self._field(form, "Similaridade", 1)
        self.cargo = self._field(form, "Cargo", 2)
        self.orgao = self._field(form, "Órgão", 3)
        self.uf = ttk.Combobox(form, values=[""], width=8)
        ttk.Label(form, text="UF").grid(row=0, column=4, sticky="w")
        self.uf.grid(row=1, column=4, padx=6)
        ttk.Button(form, text="Consultar", command=self.consultar).grid(row=1, column=5, padx=8)

        columns = ("nome", "cargo", "orgao", "uf", "situacao")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        headings = {
            "nome": "Nome",
            "cargo": "Cargo",
            "orgao": "Órgão",
            "uf": "UF",
            "situacao": "Situação",
        }
        for key, label in headings.items():
            self.tree.heading(key, text=label)
            self.tree.column(key, width=160 if key != "nome" else 240)
        self.tree.pack(fill="both", expand=True, padx=12, pady=12)
        self.status = ttk.Label(self, text="Pronto")
        self.status.pack(anchor="w", padx=12, pady=(0, 10))
        self.after(200, self._load_ufs)

    def _field(self, parent, label: str, column: int) -> ttk.Entry:
        ttk.Label(parent, text=label).grid(row=0, column=column, sticky="w", padx=6)
        entry = ttk.Entry(parent, width=22)
        entry.grid(row=1, column=column, padx=6)
        return entry

    def _load_ufs(self) -> None:
        try:
            self.uf["values"] = [""] + self.client.ufs()
        except Exception:
            self.status["text"] = "API indisponível; inicie o docker compose."

    def consultar(self) -> None:
        try:
            payload = self.client.search(
                nome=self.nome.get().strip(),
                similar=self.similar.get().strip(),
                cargo=self.cargo.get().strip(),
                orgao=self.orgao.get().strip(),
                uf=self.uf.get().strip(),
                limit=50,
            )
        except Exception as exc:
            messagebox.showerror("Consulta", str(exc))
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        for item in payload.get("items", []):
            self.tree.insert(
                "",
                "end",
                values=(
                    item["nome"],
                    item["cargo"]["descricao"],
                    item["orgao"]["sigla"],
                    item["uf"],
                    item["situacao"],
                ),
            )
        self.status["text"] = f"{payload.get('total', 0)} registro(s) encontrado(s)."


if __name__ == "__main__":
    ConsultaApp().mainloop()
