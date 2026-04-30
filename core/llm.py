# from openai import OpenAI
from groq import Groq
from core.config import GROQ_API_KEY, MODEL, TEMPERATURE, MAX_TOKENS

# client = OpenAI(api_key=OPENAI_API_KEY)
client = Groq(api_key=GROQ_API_KEY)

def call_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )

    return response.choices[0].message.content.strip()

