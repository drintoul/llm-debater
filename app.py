import streamlit as st
from styles import CUSTOM_CSS
from debate_manager import DebateManager
from ui_components import DebateUI
from time import sleep

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.current_round = 0

def start_debate(topic, model1, model2, rounds, judge_model, enable_fact_checking=False, fact_checker_model=None):
    if not topic:
        return

    st.session_state.messages = []
    st.session_state.current_round = 0

    debate = DebateManager(topic, model1, model2, judge_model, fact_checker_model if enable_fact_checking else None)

    # Container for real-time debate display
    with st.container():
        # Opening statements
        st.write("### Opening Statements")
        pro_response = debate.get_pro_opening()
        fact_check = debate.fact_check_statement(pro_response) if enable_fact_checking else None
        st.session_state.messages.append({"role": "LLM1", "content": pro_response, "model": model1, "fact_check": fact_check})
        DebateUI.display_message(pro_response, True, model1, fact_check=fact_check)

        sleep(1)

        con_response = debate.get_con_opening()
        fact_check = debate.fact_check_statement(con_response) if enable_fact_checking else None
        st.session_state.messages.append({"role": "LLM2", "content": con_response, "model": model2, "fact_check": fact_check})
        DebateUI.display_message(con_response, False, model2, fact_check=fact_check)

        sleep(1)

        # Evaluate opening round if judging is enabled
        if judge_model:
            round_result = debate.evaluate_round(pro_response, con_response)
            if round_result:
                st.write("")
                st.write("#### Score After Round 1")
                st.markdown(f'''<div class="round-score">
                    <span class="score-pro">Pro {DebateUI.format_score(debate.pro_wins)}</span>
                    <span class="score-divider">-</span>
                    <span class="score-con">{DebateUI.format_score(debate.con_wins)} Con</span>
                </div>''', unsafe_allow_html=True)

        # Subsequent rounds
        for round in range(2, rounds + 1):
            st.write(f"### Round {round}")
            pro_msg = next((msg for msg in reversed(st.session_state.messages) if msg["role"] == "LLM1"), None)
            con_msg = next((msg for msg in reversed(st.session_state.messages) if msg["role"] == "LLM2"), None)

            # Pro's turn
            pro_response = debate.get_pro_argument(con_msg["content"])
            fact_check = debate.fact_check_statement(pro_response) if enable_fact_checking else None
            st.session_state.messages.append({"role": "LLM1", "content": pro_response, "model": model1, "fact_check": fact_check})
            DebateUI.display_message(pro_response, True, model1, fact_check=fact_check)

            sleep(1)

            # Con's turn
            con_response = debate.get_con_argument(pro_response)
            fact_check = debate.fact_check_statement(con_response) if enable_fact_checking else None
            st.session_state.messages.append({"role": "LLM2", "content": con_response, "model": model2, "fact_check": fact_check})
            DebateUI.display_message(con_response, False, model2, fact_check=fact_check)

            sleep(1)

            # Evaluate round if judging is enabled
            if judge_model:
                round_result = debate.evaluate_round(pro_response, con_response)
                if round_result:
                    st.write("")
                    st.write(f"#### Score After Round {round}")
                    st.markdown(f'''<div class="round-score">
                        <span class="score-pro">Pro {DebateUI.format_score(debate.pro_wins)}</span>
                        <span class="score-divider">-</span>
                        <span class="score-con">{DebateUI.format_score(debate.con_wins)} Con</span>
                    </div>''', unsafe_allow_html=True)

            st.session_state.current_round = round

        # Final verdict
        if judge_model:
            pro_final = next((msg["content"] for msg in reversed(st.session_state.messages) if msg["role"] == "LLM1"), None)
            con_final = next((msg["content"] for msg in reversed(st.session_state.messages) if msg["role"] == "LLM2"), None)
            verdict = debate.get_final_verdict(pro_final, con_final)

            st.write("")
            st.write("---")
            st.write("### 🏆 Final Verdict")
            DebateUI.display_verdict(verdict)

def main():
    st.set_page_config(page_title="LLM Debater 🚨")
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    initialize_session_state()

    st.title("AI Debate Arena")

    # Input controls section
    with st.container():
        topic, model1, model2, rounds, enable_scoring, judge_model, enable_fact_checking, fact_checker_model = DebateUI.render_controls()

        if st.button("Start Debate", type="primary"):
            st.session_state.topic_content = topic
            start_debate(
                topic,
                model1,
                model2,
                rounds,
                judge_model if enable_scoring else None,
                enable_fact_checking,
                fact_checker_model
            )

if __name__ == "__main__":
    main()
