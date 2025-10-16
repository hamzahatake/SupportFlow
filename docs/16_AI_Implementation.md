## AI Implementation (step by step)

### 1) Provider interface
```python
# ai/provider.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class IntentRequest:
    title: str
    body: str
    org_id: int

@dataclass
class IntentResponse:
    category: Optional[str]
    priority: Optional[str]
    confidence: float

class AIProvider:
    def classify_intent(self, req: IntentRequest) -> IntentResponse:
        raise NotImplementedError
```

### 2) OpenAI adapter (example)
```python
# ai/providers/openai_adapter.py
import os
from openai import OpenAI
from ai.provider import AIProvider, IntentRequest, IntentResponse

class OpenAIProvider(AIProvider):
    def __init__(self):
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def classify_intent(self, req: IntentRequest) -> IntentResponse:
        prompt = (
            "You classify tickets. Categories: billing, technical, account, other. "
            "Priority: low, medium, high, vip. Return JSON with category, priority, confidence (0-1).\n"
            f"Title: {req.title}\nBody: {req.body}\n"
        )
        out = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        # TODO: parse JSON from out.choices[0].message.content
        return IntentResponse(category=None, priority=None, confidence=0.0)
```

### 3) Redaction rules (simple)
- Mask emails: replace `name@example.com` with `[REDACTED_EMAIL]`.
- Mask phone numbers: replace patterns with `[REDACTED_PHONE]`.
- Do not send attachments; only text.

### 4) API endpoint
- POST /api/ai/intent
- Input: { title, body }
- Output: { category, priority, confidence }
- Use org from JWT; check feature flag `AI_INTENT_ENABLED`.

### 5) Errors, retries, limits
- If provider fails: return 503 with friendly message.
- Retry up to 2 times (exponential backoff) in background if needed.
- Throttle: 60 requests/minute per organization.

### 6) Logging and cost
- Create `AILog` row with request/response (with redaction) and latency.
- Add daily summary: calls, cost estimate, error rate.


