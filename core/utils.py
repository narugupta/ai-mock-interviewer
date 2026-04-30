import json
import re


# ✅ Load prompt from file
def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ✅ Safe JSON parsing (Groq-safe)
def safe_json_parse(text: str):
    try:
        return json.loads(text)
    except:
        # Extract JSON block if model adds extra text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    # fallback default
    return {
        "clarity": 5,
        "depth": 5,
        "structure": 5,
        "confidence": 5,
        "strengths": [],
        "weaknesses": ["Could not parse evaluation"],
        "follow_up_needed": False,
        "suggested_followup": ""
    }