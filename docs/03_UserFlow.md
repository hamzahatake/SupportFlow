## User Flow (simple)

1) Company joins and creates an organization.
2) Admin or Supervisor invites agents and customers.
3) Customer submits a ticket (web form).
4) Agent sees the ticket in their queue.
5) Agent replies. Customer gets an email.
6) Agent marks ticket as solved.
7) Supervisor views basic metrics.

Notes:
- If AI is on: on ticket create, it can suggest category/priority.
- If AI is on: agent can click "Suggest reply" to get a draft.

### Error / Edge Flows
- Invalid login -> show message, do not reveal which field.
- Invite expired -> show message and allow new invite request.
- No permission -> show "Not allowed" and link back.
- File too large -> show clear error; allow retry.

### Escalation Flow (simple)
- If no reply in X hours: add reminder (email) and flag ticket.
- If still no reply: auto-assign to available agent or escalate to supervisor.


