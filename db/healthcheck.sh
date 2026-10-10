#!/bin/sh
pg_isready -U "${POSTGRES_USER:-app}" -d "${POSTGRES_DB:-servidores}"
