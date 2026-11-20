# SiteCheck

SiteCheck is a passive uptime monitor and security audit application for authorised website owners.

## Local development

```bash
python -m venv .venv
.venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## Docker

```bash
cp .env.example .env
docker compose up --build
```

Open http://localhost:8000/healthz.
