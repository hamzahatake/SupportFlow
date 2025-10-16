## API Endpoints (draft)

### Auth
- POST /api/auth/login
- POST /api/auth/logout
- POST /api/auth/refresh
- POST /api/auth/password-reset
- POST /api/auth/password-reset/confirm

### Users
- GET /api/users/me
- GET /api/users
- POST /api/users (admin/supervisor)
- GET /api/users/{id}
- PATCH /api/users/{id}

### Organizations & Departments
- GET/POST /api/orgs
- GET/POST /api/departments

### Tickets
- GET/POST /api/tickets
- GET/PATCH /api/tickets/{id}
- POST /api/tickets/{id}/messages
- POST /api/tickets/{id}/assign
- POST /api/tickets/{id}/resolve
- POST /api/tickets/{id}/reopen

### AI (optional)
- POST /api/ai/intent            -> category, priority, confidence
- POST /api/ai/suggest-reply     -> drafts
- POST /api/ai/autotag           -> tags

Notes:
- All requests are scoped to the user's organization.
- Use JWT in Authorization header: "Bearer <token>".

### Request/Response Examples

Ticket create (request):
```json
{
  "title": "Payment failed on checkout",
  "body": "I see error code 402 when paying.",
  "priority": "high",
  "category": "billing",
  "tags": ["payments", "stripe"]
}
```

Ticket (response):
```json
{
  "id": 123,
  "title": "Payment failed on checkout",
  "body": "I see error code 402 when paying.",
  "status": "open",
  "priority": "high",
  "category": "billing",
  "assigned_to": null,
  "created_at": "2025-10-16T12:00:00Z"
}
```

Error shape (example):
```json
{
  "detail": "Not allowed"
}
```

### Permissions & Throttling (high level)
- Customers: CRUD only own tickets.
- Agents: read all org tickets; update assigned.
- Supervisor: assign/unassign, manage departments.
- Throttles: ticket create 5/min/user; AI endpoints 60/min/org.


