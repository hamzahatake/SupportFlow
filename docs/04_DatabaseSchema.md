## Database Schema (draft)

### Main Tables / Models
- Organization
  - name, slug, plan, settings
- Department
  - name, description, is_active, created_by
- User
  - email, password, role, organization, phone_number, timezone
- Customer (profile for user with role=customer)
  - user, company, priority_level, notes
- Agent (profile for user with role=agent)
  - user, department, skills, is_available
- Supervisor (profile for user with role=supervisor)
  - user, department, can_create_agents

### Ticket Models (to add)
- Ticket
  - organization, created_by (customer), assigned_to (agent)
  - title, body
  - status: open | pending | solved | closed
  - priority: low | medium | high | vip
  - category: billing | technical | account | other
  - tags: M2M TicketTag
  - sla_due_at, first_response_at, resolved_at, closed_at
  - is_spam (bool), source: web | email
- TicketMessage
  - ticket, author (user), text, is_internal
- Attachment
  - ticket_message, file_path, size, mime_type
- TicketEvent (audit)
  - ticket, type, data, created_at
 - TicketStatusHistory
  - ticket, from_status, to_status, changed_by, created_at
 - TicketTag
  - name (unique per org), organization

### Relationships
- One Organization has many Users, Departments, Tickets.
- One Department has many Agents and Supervisors.
- One Ticket has many TicketMessages and TicketEvents.

### Indexes (examples)
- Ticket: (organization, status), (organization, assigned_to, status), trigram on title (if Postgres).
- TicketMessage: (ticket, created_at).

### Constraints
- `assigned_to.organization == ticket.organization`.
- Attachment size limit (e.g., <= 5MB) and allowed types (png, jpg, pdf, txt).


