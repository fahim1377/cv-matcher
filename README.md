# CV-Matcher

FastAPI-Service, der einen Lebenslauf mit einer Stellenanzeige per Embedding vergleicht, einen Match-Score berechnet und fehlende Skills aufzeigt.

## Setup

```bash
uv sync
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

## Roadmap

- [x] Fundament: Projektstruktur, Tooling (`uv`, `ruff`, `mypy`), Health-Check-Endpoint
- [ ] JWT-Auth, Dependency Injection, PostgreSQL + SQLAlchemy + Alembic, Matching-Logik, vollständige Test-Coverage
- [ ] Docker Compose (FastAPI + PostgreSQL), GitHub Actions CI
- [ ] Redis-Caching für Embeddings
