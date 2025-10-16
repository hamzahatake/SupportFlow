## AI Overview (simple)

### What AI can do here
- Intent: guess category and priority for a new ticket.
- Suggested reply: draft a short answer for the agent.
- Auto-tag: add tags from the text.
- Similar tickets: show related tickets to avoid duplicates.

### Human in the loop
- AI only suggests. Agent decides.
- Show confidence (0-1). If low, do nothing.

### Rollout plan
- Start with Intent only.
- Then add Suggested reply.
- Add Auto-tag later.
- Similar tickets last (needs search index).

### Feature flags (ENV)
- AI_INTENT_ENABLED=1
- AI_SUGGEST_REPLY_ENABLED=0
- AI_AUTOTAG_ENABLED=0
- AI_SIMILAR_ENABLED=0


