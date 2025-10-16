## AI Evaluation

### What to measure
- Acceptance rate: agent uses suggestion without big edits.
- Edit distance: how much the draft changed.
- Latency: time to get AI response.
- Cost: $ per 1000 calls (estimate from tokens).

### How to collect
- Log each suggestion with ID.
- When agent accepts/edits, store action and edit length.
- Daily job: aggregate metrics per org and feature.

### A/B testing (simple)
- Feature flag 50% on, 50% off per org.
- Compare acceptance and time saved.

### Offline eval set
- Save 50 real tickets (redacted) and expected categories.
- Run model weekly; track accuracy and drift.


