#!/usr/bin/env bash
set -euo pipefail
python3 -m pip install -r requirements.txt pyinstaller
pyinstaller --onefile --name consulta-servidores app.py
echo "Binário gerado em dist/consulta-servidores"
