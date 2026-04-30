from core.llm import call_llm
from core.utils import load_prompt


class CoachAgent:
    def __init__(self):
        self.prompt = load_prompt("prompts/coach.txt")

    def generate_feedback(self, transcript: str) -> str:
        user_prompt = f"""
Here is the full interview transcript and evaluations:

{transcript}
"""
        return call_llm(self.prompt, user_prompt)