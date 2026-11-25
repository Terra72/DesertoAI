import anthropic
import os
import json

from deserto.config import SUMMARIZE_MODEL

SYSTEM_PROMPT = """
You are an environmental research assistant.

You are tracking desertification protection practices globally.

Be conservative. Only claim change if the evidence meaningfully adds
new knowledge or contradicts existing understanding.
"""

def summarize(item, current_summary):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""
Current global summary:
{current_summary or "(empty)"}

New source:
Title: {item['title']}
Summary: {item['summary']}
Source: {item['source']}

Respond in JSON with:
- "novel": true or false
- "update": a 1–2 sentence update if novel, otherwise ""
"""

    response = client.messages.create(
        model=SUMMARIZE_MODEL,
        max_tokens=300,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,  # deterministic
    )

    content = response.content[0].text

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Failed to parse LLM response:")
        print(content)
        return {
            "novel": False,
            "update": ""
        }

