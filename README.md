# CV-Matcher

FastAPI-Service, der einen Lebenslauf mit einer Stellenanzeige per Embedding vergleicht, einen Match-Score berechnet und fehlende Skills aufzeigt.

## Setup

Voraussetzung: eine laufende PostgreSQL-Instanz mit einer `cv_matcher`- und einer `cv_matcher_test`-Datenbank (siehe `.env.example` für die erwartete Verbindungs-URL).

```bash
uv sync
cp .env.example .env   # Werte anpassen (Datenbank-Zugangsdaten, JWT_SECRET_KEY via `openssl rand -hex 32`)
uv run alembic upgrade head
uv run uvicorn cv_matcher.main:app --reload
```

API-Dokumentation danach unter `http://localhost:8000/docs`.

## Tests

```bash
uv run pytest
```

## Lint & Type-Checking

```bash
uv run ruff check .
uv run mypy src
```

## Datenbank-Migrationen

```bash
uv run alembic revision --autogenerate -m "beschreibung"
uv run alembic upgrade head
```

## Roadmap

- [x] Fundament: Projektstruktur, Tooling (`uv`, `ruff`, `mypy`), Health-Check-Endpoint
- [x] Auth (JWT), Dependency Injection, PostgreSQL + SQLAlchemy (async) + Alembic, vollständige Test-Coverage
- [ ] CV/Job-Matching-Logik (Embeddings via `sentence-transformers`)
- [ ] Docker Compose (FastAPI + PostgreSQL), GitHub Actions CI
- [ ] Redis-Caching für Embeddings
