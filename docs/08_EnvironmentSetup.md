## Environment Setup

### Folder Structure (backend)
- support_dashboard/ (Django project)
- users/, tickets/ (apps)
- docs/

### .env variables (example)
- SECRET_KEY=
- DEBUG=1
- POSTGRES_DB=
- POSTGRES_USER=
- POSTGRES_PASSWORD=
- POSTGRES_HOST=localhost
- POSTGRES_PORT=5432
- USE_SQLITE=1  (set to 1 for local sqlite)
- OPENAI_API_KEY= (if using AI)
 - EMAIL_HOST=localhost
 - EMAIL_PORT=1025
 - DEFAULT_FROM_EMAIL=no-reply@example.com

### Commands
- python -m venv .venv && source .venv/bin/activate (or Windows PowerShell equivalent)
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver

### Tips
- Create `.env.example` and keep real `.env` out of Git.
- Use `DEBUG=0` in production.


