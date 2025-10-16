## Deployment Plan (basic)

### Hosting
- Backend: Render, Railway, or Fly.io
- DB: Managed Postgres (Neon, Supabase, Railway)
- Frontend: Vercel or Netlify

### Steps
- Push to Git (main and feature branches)
- Create production `.env` (never commit)
- Run migrations
- Set up HTTPS and CORS

### Notes
- Start with one region.
- Add monitoring (logs, error tracking) later.

### CI/CD (simple)
- On PR: run lint, tests, type check (optional), build.
- On main: deploy to staging; run migrations; smoke test; then promote to prod.

### Storage
- Static assets: served by CDN or app server (small scale ok).
- Media uploads: S3-compatible storage in prod.


