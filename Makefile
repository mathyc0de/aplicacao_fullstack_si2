.PHONY: up down test load-test desktop

up:
	docker compose up --build

down:
	docker compose down

test:
	cd backend && python3 -m pytest

load-test:
	python3 backend/scripts/load_test.py

desktop:
	cd desktop && python3 app.py
reset-db:
	docker compose down -v
