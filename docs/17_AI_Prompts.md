## AI Prompt Templates

### Style
- Be short and clear.
- Ask for strict JSON when needed.
- Set categories and priorities in the prompt.

### Intent (JSON)
```
SYSTEM: You are a helpful support assistant. Be concise.
USER: Classify this ticket.
Title: {title}
Body: {body}

Return JSON: {"category": one of ["billing","technical","account","other"], "priority": one of ["low","medium","high","vip"], "confidence": 0..1}
```

### Suggested reply
```
SYSTEM: You write short, polite support replies.
USER: Write a reply to this message. Keep it under 120 words.
Thread:
{conversation_text}
```

### Auto-tag
```
SYSTEM: Extract 3-6 short tags.
USER: From the text, return comma-separated tags only.
Text: {text}
```

### Summary
```
SYSTEM: Summarize the conversation for an agent.
USER: Give a brief 3-5 bullet summary.
Thread:
{conversation_text}
```


