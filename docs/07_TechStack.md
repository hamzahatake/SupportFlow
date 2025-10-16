## Tech Stack

### Backend
- Python, Django, Django REST Framework
- JWT auth (SimpleJWT)
- PostgreSQL (prod), SQLite (local ok)

### Frontend
- React + React Router
- Fetch or Axios for API calls

### Realtime & Tasks (later)
- Channels (WebSocket) with Redis
- Celery + Redis for background jobs

### AI (optional)
- Provider SDK (OpenAI or Anthropic) via an adapter

### Tooling
- drf-spectacular for API schema and Swagger UI
- Pre-commit (black/ruff/isort) or flake8 + black
- pytest + pytest-django
- Sentry (errors), Loguru/structlog (logs)


