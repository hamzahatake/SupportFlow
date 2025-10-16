## Status Transitions and SLA

### Ticket Status
- open
- pending
- solved
- closed

### Allowed Transitions
- open -> pending | solved
- pending -> solved | open
- solved -> closed | open
- closed -> open (only admin/supervisor)

### Rules
- First agent reply sets `first_response_at`.
- When status becomes solved, set `resolved_at`.
- When status becomes closed, set `closed_at`.

### SLA (simple)
- `sla_due_at = created_at + plan_based_duration`.
- If now > sla_due_at and not solved: mark "at risk" and notify.


