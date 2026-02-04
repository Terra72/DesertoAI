from openai import OpenAI
import os
import json

client = OpenAI()

SYSTEM_PROMPT = """
You are an environmental research assistant.

You are tracking desertification protection practices globally.

Be conservative. Only claim change if the evidence meaningfully adds
new knowledge or contradicts existing understanding.
"""

def summarize(item, current_summary):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0, # deterministic
        response_format={ "type": "json_object" }
    )

    content = response.choices[0].message.content

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Failed to parse LLM response:")
        print(content)
        return {
            "novel": False,
            "update": ""
        }

