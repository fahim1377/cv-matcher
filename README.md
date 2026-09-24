# CV-Matcher

FastAPI-Service, der einen Lebenslauf mit einer Stellenanzeige per Embedding vergleicht und einen Match-Score berechnet.

## Setup

Voraussetzung: eine laufende PostgreSQL-Instanz mit einer `cv_matcher`- und einer `cv_matcher_test`-Datenbank (siehe `.env.example` für die erwartete Verbindungs-URL) sowie der [pgvector](https://github.com/pgvector/pgvector)-Extension:

```bash
# einmalig, als Postgres-Superuser (nicht die App-Rolle)
CREATE EXTENSION IF NOT EXISTS vector;   -- in cv_matcher UND cv_matcher_test ausfuehren
```

```bash
uv sync
cp .env.example .env   # Werte anpassen (Datenbank-Zugangsdaten, JWT_SECRET_KEY via `openssl rand -hex 32`)
uv run alembic upgrade head
uv run uvicorn cv_matcher.main:app --reload
```

API-Dokumentation danach unter `http://localhost:8000/docs`.

Hinweis: Beim ersten Start bzw. ersten `POST /cv`- oder `/jobs`-Aufruf wird das Embedding-Modell (`paraphrase-multilingual-MiniLM-L12-v2`, ~470 MB) einmalig heruntergeladen.

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
- [x] CV/Job-Matching per Embeddings (`sentence-transformers`, mehrsprachig) + pgvector-Cosine-Similarity
- [ ] Skill-Gap-Analyse (fehlende Skills zwischen CV und Job auflisten)
- [ ] Docker Compose (FastAPI + PostgreSQL), GitHub Actions CI
- [ ] Redis-Caching für Embeddings
