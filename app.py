import streamlit as st
from styles import CUSTOM_CSS
from config import AVAILABLE_MODELS
from debate_manager import DebateManager
from llm_service import LLMService
from ui_components import DebateUI

def build_transcript():
    names = {"LLM1": "Pro", "LLM2": "Con"}
    return "\n".join(f"{names.get(m['role'], m['role'])}: {m['content']}" for m in st.session_state.messages)

def render_log_entry(entry):
    kind = entry["type"]
    if kind == "heading":
        st.write(entry["text"])
    elif kind == "divider":
        st.write("---")
    elif kind == "message":
        DebateUI.display_message(entry["content"], entry["role"] == "LLM1", entry["model"], fact_check=entry["fact_check"])
    elif kind == "score":
        st.write(f"#### Score After Round {entry['round']}")
        reason_html = f'<div class="score-reason">{entry["reason"]}</div>' if entry["reason"] else ""
        st.markdown(f'''<div class="round-score">
            <span class="score-pro">Pro {DebateUI.format_score(entry["pro"])}</span>
            <span class="score-divider">-</span>
            <span class="score-con">{DebateUI.format_score(entry["con"])} Con</span>
            {reason_html}
        </div>''', unsafe_allow_html=True)
    elif kind == "verdict":
        DebateUI.display_verdict(entry["text"])

def export_markdown():
    """Render the stored debate log as a Markdown transcript for download."""
    names = {"LLM1": "Pro", "LLM2": "Con"}
    lines = ["# Debate Transcript", "", f"**Topic:** {st.session_state.get('topic_content', '')}", ""]
    for e in st.session_state.get("debate_log", []):
        kind = e["type"]
        if kind == "heading":
            lines.append(e["text"])
        elif kind == "divider":
            lines.append("---")
        elif kind == "message":
            lines.append(f"**{names.get(e['role'], e['role'])} ({e['model']}):** {e['content']}")
            if e["fact_check"]:
                lines.append(f"> 🔍 *Fact check:* {e['fact_check']}")
        elif kind == "score":
            lines.append(f"**Score after Round {e['round']}: Pro {DebateUI.format_score(e['pro'])} – {DebateUI.format_score(e['con'])} Con**")
            if e["reason"]:
                lines.append(f"*{e['reason']}*")
        elif kind == "verdict":
            lines.append(f"**🏆 {e['text']}**")
        lines.append("")
    return "\n".join(lines)

def start_debate(topic, model1, model2, rounds, judge_model, enable_fact_checking=False, fact_checker_model=None, response_length="sentence"):
    if not topic:
        return

    st.session_state.messages = []
    st.session_state.debate_log = []

    def emit(entry):
        st.session_state.debate_log.append(entry)
        render_log_entry(entry)

    def take_turn(token_stream, role, model):
        """Stream a debater's reply into its bubble, record it, return cleaned text (or None on error)."""
        raw = DebateUI.stream_message(token_stream, is_pro=(role == "LLM1"), model=model)
        text = LLMService._cleanup(raw)
        if text.startswith("Error:"):
            st.error(f"{model}: {text}")
            return None
        st.session_state.messages.append({"role": role, "content": text, "model": model, "fact_check": None})
        st.session_state.debate_log.append({"type": "message", "role": role, "content": text, "model": model, "fact_check": None})
        return text

    def attach_fact_check(statement, role):
        with st.spinner("Fact-checking…"):
            fact_check = debate.fact_check_statement(statement)
        DebateUI.display_fact_check(fact_check, role == "LLM1")
        st.session_state.messages[-1]["fact_check"] = fact_check
        st.session_state.debate_log[-1]["fact_check"] = fact_check

    def judge_round(pro_arg, con_arg, round_num):
        if not judge_model:
            return
        with st.spinner("Judge is scoring this round…"):
            reason = debate.evaluate_round(pro_arg, con_arg)
        if reason is not None:
            emit({"type": "score", "round": round_num, "pro": debate.pro_wins, "con": debate.con_wins, "reason": reason})

    debate = DebateManager(topic, model1, model2, judge_model, fact_checker_model if enable_fact_checking else None, response_length)

    with st.container():
        # Opening statements
        emit({"type": "heading", "text": "### Opening Statements"})

        pro_response = take_turn(debate.stream_pro_opening(), "LLM1", model1)
        if pro_response is None:
            return
        if enable_fact_checking:
            attach_fact_check(pro_response, "LLM1")

        con_response = take_turn(debate.stream_con_opening(), "LLM2", model2)
        if con_response is None:
            return
        if enable_fact_checking:
            attach_fact_check(con_response, "LLM2")

        judge_round(pro_response, con_response, 1)

        # Subsequent rounds
        for round_num in range(2, rounds + 1):
            emit({"type": "heading", "text": f"### Round {round_num}"})
            transcript = build_transcript()

            pro_response = take_turn(debate.stream_pro_argument(con_response, transcript), "LLM1", model1)
            if pro_response is None:
                return
            if enable_fact_checking:
                attach_fact_check(pro_response, "LLM1")

            con_response = take_turn(debate.stream_con_argument(pro_response, transcript), "LLM2", model2)
            if con_response is None:
                return
            if enable_fact_checking:
                attach_fact_check(con_response, "LLM2")

            judge_round(pro_response, con_response, round_num)

        # Final verdict
        if judge_model:
            with st.spinner("Judge is writing the final verdict…"):
                verdict = debate.get_final_verdict()
            if verdict.startswith("Error:"):
                st.error(f"{judge_model}: {verdict}")
                return
            emit({"type": "divider"})
            emit({"type": "heading", "text": "### Final Verdict"})
            emit({"type": "verdict", "text": verdict})

def main():
    st.set_page_config(page_title="LLM Debater 🚨", layout="wide")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    st.session_state.setdefault("messages", [])

    if not AVAILABLE_MODELS:
        st.error("No models configured — set AVAILABLE_MODELS in your .env file.")
        st.stop()

    st.title("AI Debate Arena")
    st.caption("Two local LLMs argue opposite sides of a topic, turn by turn — with optional AI judging and fact-checking, all running on your own Ollama server.")

    # Input controls section
    with st.container():
        topic, model1, model2, rounds, response_length, enable_scoring, judge_model, enable_fact_checking, fact_checker_model, server_online = DebateUI.render_controls()

        if not server_online:
            st.error("⚠️ Ollama Server is offline. Please check the sidebar for details.")

        start_button = st.button(
            "Start Debate",
            type="primary",
            disabled=not server_online,
            help="Ollama server must be online to start debate" if not server_online else None
        )
        st.caption("⏳ First responses may take a while — Ollama loads each model into memory on first use. Please be patient.")

        if start_button and server_online:
            st.session_state.topic_content = topic
            start_debate(
                topic,
                model1,
                model2,
                rounds,
                judge_model if enable_scoring else None,
                enable_fact_checking,
                fact_checker_model,
                "sentence" if response_length == "One sentence" else "paragraph"
            )
        elif st.session_state.get("debate_log"):
            # Replay the last debate so it survives widget interactions / reruns
            for entry in st.session_state.debate_log:
                render_log_entry(entry)

    if st.session_state.get("debate_log"):
        st.download_button(
            "Download Transcript",
            export_markdown(),
            file_name="debate_transcript.md",
            mime="text/markdown",
            help="Save the full debate — arguments, fact checks, scores, and verdict — as a Markdown file."
        )

if __name__ == "__main__":
    main()
