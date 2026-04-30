from core.llm import call_llm
from core.utils import load_prompt


class InterviewerAgent:
    def __init__(self):
        self.prompt = load_prompt("prompts/interviewer.txt")

    def ask_question(self, role, focus, background, history, hint=None):
        user_prompt = f"""
Role: {role}
Focus: {focus}
Background: {background}

Conversation:
{history}

Hint (if any): {hint}

Generate the next question.
"""
        return call_llm(self.prompt, user_prompt)