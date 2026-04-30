import sys
import os

# Fix import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from orchestrator import InterviewOrchestrator

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AI Mock Interview Coach", layout="wide")
st.title("🎤 AI Mock Interview Coach")

# ---------------- SIDEBAR ----------------
role = st.sidebar.text_input("Target Role", "Frontend Engineer Intern")
focus = st.sidebar.selectbox("Focus Area", ["technical", "behavioral", "mixed"])
background = st.sidebar.text_area("Background", "Built React apps")

start = st.sidebar.button("Start Interview")

# ---------------- SESSION STATE ----------------
if "orch" not in st.session_state:
    st.session_state.orch = InterviewOrchestrator()

if "history" not in st.session_state:
    st.session_state.history = ""

if "question" not in st.session_state:
    st.session_state.question = None

if "turn" not in st.session_state:
    st.session_state.turn = 0

if "chat" not in st.session_state:
    st.session_state.chat = []

if "running" not in st.session_state:
    st.session_state.running = False

if "last_eval" not in st.session_state:
    st.session_state.last_eval = None

# ---------------- START ----------------
if start:
    st.session_state.orch = InterviewOrchestrator()
    st.session_state.history = ""
    st.session_state.question = None
    st.session_state.turn = 0
    st.session_state.chat = []
    st.session_state.running = True
    st.session_state.last_eval = None

# ---------------- MAIN ----------------
MAX_TURNS = 5

if st.session_state.running:

    orch = st.session_state.orch

    # st.sidebar.markdown(f"### Turn: {st.session_state.turn + 1}/{MAX_TURNS}")

    # ---------------- END CONDITION ----------------
    if st.session_state.turn >= MAX_TURNS:
        st.success("Interview completed!")

        with st.spinner("Generating final feedback..."):
            transcript = orch.memory.format_full_transcript()
            feedback = orch.coach.generate_feedback(transcript)

        st.markdown("##Final Feedback")
        st.markdown(feedback)

        st.session_state.running = False
        st.stop()

    # ---------------- GENERATE QUESTION ----------------
    if st.session_state.question is None:
        with st.spinner("Generating question..."):
            
            # ADAPTIVE LOGIC ADDED HERE 
            hint = None
            if st.session_state.last_eval:
                eval_data = st.session_state.last_eval
                
                # Safely calculate average score, defaulting to 5 if keys are missing
                avg_score = (
                    eval_data.get("clarity", 5) + 
                    eval_data.get("depth", 5) + 
                    eval_data.get("structure", 5) + 
                    eval_data.get("confidence", 5)
                ) / 4
                
                if eval_data.get("follow_up_needed"):
                    hint = f"Ask a follow-up: {eval_data.get('suggested_followup', '')}"
                elif avg_score > 7:
                    hint = "Increase difficulty"
                elif avg_score < 5:
                    hint = "Simplify or probe basics"

            # Pass the hint to the interviewer
            st.session_state.question = orch.interviewer.ask_question(
                role,
                focus,
                background,
                st.session_state.history,
                hint
            )

    question = st.session_state.question

    # ---------------- CHAT HISTORY ----------------
    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])

    # ---------------- CURRENT QUESTION ----------------
    st.chat_message("assistant").write(question)

    # ---------------- USER INPUT ----------------
    answer = st.chat_input("Type your answer here...")

    if answer:
        # Show user answer
        st.chat_message("user").write(answer)

        # Save chat
        st.session_state.chat.append({"role": "assistant", "content": question})
        st.session_state.chat.append({"role": "user", "content": answer})

        # ---------------- EVALUATION ----------------
        with st.spinner("Evaluating..."):
            evaluation = orch.evaluator.evaluate(question, answer)

        st.session_state.last_eval = evaluation

        # Store in memory
        orch.memory.add_turn(question, answer, evaluation)
        st.session_state.history = orch.memory.format_for_prompt()

        # Move to next turn
        st.session_state.turn += 1
        st.session_state.question = None

        st.rerun()

    # ---------------- SHOW LAST EVALUATION (AFTER RERUN) ----------------
    if st.session_state.last_eval:
        st.markdown("### Last Evaluation")
        st.json(st.session_state.last_eval)