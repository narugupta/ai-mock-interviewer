from agents.interviewer import InterviewerAgent
from agents.evaluator import EvaluatorAgent
from agents.coach import CoachAgent
from core.memory import Memory


class InterviewOrchestrator:
    def __init__(self):
        self.interviewer = InterviewerAgent()
        self.evaluator = EvaluatorAgent()
        self.coach = CoachAgent()
        self.memory = Memory()

    def run(self, role, focus, background):
        print("\n🎤 Starting Mock Interview...\n")

        NUM_TURNS = 6

        for turn in range(NUM_TURNS):
            print(f"\n--- Turn {turn+1} ---\n")

            history = self.memory.format_for_prompt()
            last_eval = self.memory.get_last_evaluation()

            hint = None

            # Adaptive logic
            if last_eval:
                avg_score = (
                    last_eval["clarity"] +
                    last_eval["depth"] +
                    last_eval["structure"] +
                    last_eval["confidence"]
                ) / 4

                if last_eval["follow_up_needed"]:
                    hint = f"Ask a follow-up: {last_eval['suggested_followup']}"
                elif avg_score > 7:
                    hint = "Increase difficulty"
                elif avg_score < 5:
                    hint = "Simplify or probe basics"

            # Ask question
            question = self.interviewer.ask_question(
                role, focus, background, history, hint
            )

            print(f"Interviewer: {question}")

            answer = input("\nYour answer: ")

            # Evaluate
            evaluation = self.evaluator.evaluate(question, answer)

            print("\n📊 Evaluation:")
            print(evaluation)

            # Store
            self.memory.add_turn(question, answer, evaluation)

        print("\n🎯 Generating Final Feedback...\n")

        # 🔥 Coach phase
        transcript = self.memory.format_full_transcript()
        feedback = self.coach.generate_feedback(transcript)

        print("\n🧑‍🏫 Final Feedback:\n")
        print(feedback)

        print("\n✅ Interview Completed!\n")