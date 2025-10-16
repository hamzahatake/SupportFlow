## Core Features

### Must-have (MVP)
- User login with JWT (email + password).
- Roles: customer, agent, supervisor, admin.
- Organizations (each company has its own space).
- Create and manage tickets (title, body, status, priority).
- Assign tickets to agents.
- List and filter tickets (by status, priority, assignee).
- Basic email for password reset.
- Basic supervisor dashboard (counts only).

### Nice-to-have (later)
- Real-time updates (WebSocket).
- AI suggested replies.
- AI auto-categorize and auto-tags.
- SLA rules and auto-escalation.
- Knowledge base search.
- Billing plans (free vs paid with AI).

### Acceptance Criteria (MVP)
- Auth: Login, refresh, logout work; invalid creds return 401.
- Tickets: Create, read, update status; filter by status; pagination 10/page.
- Assign: Supervisor can assign/unassign; agent sees "My tickets".
- Roles: Customer can only see own tickets; agent scoped to org; admin full org access.
- Email: Password reset sends link in dev; no errors on send.


