"""PreToolUse hook: block any tool call that mentions a .env file."""
import json
import re
import sys

# .env, .env.local, dir/.env ... but not .env.example/.sample/.template
ENV = re.compile(r"(?<![\w.-])\.env(?!\.(?:example|sample|template)\b)(?:\.[\w.-]+)?(?![\w-])", re.I)


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from strings(v)


payload = json.load(sys.stdin)
if any(ENV.search(s) for s in strings(payload.get("tool_input", {}))):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Blocked: .env files are off limits to Claude.",
    }}))
