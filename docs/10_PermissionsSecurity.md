## Permissions and Security

### Role Matrix (summary)
- Customer
  - Create tickets (self). Read own tickets. Add messages to own tickets.
- Agent
  - Read org tickets. Update assigned tickets. Add internal/public messages.
- Supervisor
  - All agent rights + assign/unassign tickets; manage departments.
- Admin
  - Full access in organization.

### Organization Scoping
- All queries must filter by `request.user.organization_id`.
- Deny access if object.organization != user.organization.

### Department Scoping
- Agents/Supervisors can list users only in their department (when needed).

### Object-Level Checks (examples)
- Customers cannot view or update other customers’ tickets.
- Agents cannot assign outside their organization.

### API Security
- JWT in `Authorization: Bearer <token>`.
- Throttling on sensitive endpoints (login, ticket create, AI).
- CORS restricted to front-end origin.

### Data Protection
- Validate and sanitize user input (strip HTML where needed).
- File uploads: size/type limits; scan if possible.
- Secrets in environment only; never commit.


