from core.llm import call_llm
from core.utils import load_prompt, safe_json_parse


class EvaluatorAgent:
    def __init__(self):
        self.prompt = load_prompt("prompts/evaluator.txt")

    def evaluate(self, question: str, answer: str) -> dict:
        user_prompt = f"""
Question:
{question}

Answer:
{answer}
"""

        response = call_llm(self.prompt, user_prompt)
        return safe_json_parse(response)