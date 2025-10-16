## Test Plan

### Scope
- Models: User, Organization, Ticket, TicketMessage, Attachment, StatusHistory.
- APIs: Auth, Users, Tickets, AI.
- Permissions: role checks and org scoping.

### Strategy
- Unit tests for models/serializers/permissions.
- API tests with DRF `APIClient`.
- Mock external: email backend, AI provider, storage.

### Cases (examples)
- Auth: login ok/invalid, refresh, logout.
- Tickets: create (customer), assign (supervisor), update status, list filters.
- Permissions: customer blocked from other org ticket; agent update only assigned.
- Attachments: reject large file; accept allowed type.
- AI: mock provider low-confidence and success.

### CI
- Run tests on PR; fail if coverage < 75% (target 85% later).


