## Non-Functional Requirements

### Performance
- p95 latency < 250ms for main endpoints (tickets list, show, create).
- DB queries per request: target <= 10 for list/detail (use select_related/prefetch_related).

### Reliability
- Background jobs must retry on failure (Celery retries).
- Idempotent endpoints for status changes.

### Observability
- Structured logs with request ID.
- Error tracking (Sentry) in prod.
- Basic metrics (requests, errors) — later add Prometheus/Otel.

### Security
- Throttling for auth and create endpoints.
- Strong password policy (Django validators).
- CORS limited; HTTPS only in prod.


