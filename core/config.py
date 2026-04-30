import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# MODEL = "gpt-4o-mini"  # fast + cheap for iteration
MODEL = "llama-3.1-8b-instant"  # best balance
TEMPERATURE = 0.7
MAX_TOKENS = 400
