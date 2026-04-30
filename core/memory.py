class Memory:
    def __init__(self):
        self.history = []

    def add_turn(self, question, answer, evaluation):
        self.history.append({
            "question": question,
            "answer": answer,
            "evaluation": evaluation
        })

    def format_for_prompt(self):
        if not self.history:
            return "No prior conversation."

        formatted = ""
        for i, turn in enumerate(self.history):
            formatted += f"""
Turn {i+1}:
Interviewer: {turn['question']}
Candidate: {turn['answer']}
"""
        return formatted.strip()

    def format_full_transcript(self):
        """Includes evaluations (for coach)"""
        if not self.history:
            return "No interview data."

        formatted = ""
        for i, turn in enumerate(self.history):
            eval_data = turn["evaluation"]
            formatted += f"""
Turn {i+1}:
Question: {turn['question']}
Answer: {turn['answer']}

Evaluation:
- Clarity: {eval_data.get('clarity')}
- Depth: {eval_data.get('depth')}
- Structure: {eval_data.get('structure')}
- Confidence: {eval_data.get('confidence')}
- Strengths: {eval_data.get('strengths')}
- Weaknesses: {eval_data.get('weaknesses')}
"""
        return formatted.strip()

    def get_last_evaluation(self):
        if not self.history:
            return None
        return self.history[-1]["evaluation"]