import streamlit as st
import requests
import json
import os
from time import sleep

def get_llm_response(prompt, model):
    url = f"{os.getenv('OLLAMA_HOST', 'http://10.27.10.200:11434')}/api/generate"

    data = {
        "model": model,
        "prompt": prompt + " Respond with exactly one sentence.",
        "stream": False,
    }

    try:
        response = requests.post(url, json=data)
        return response.json()["response"]
    except Exception as e:
        return f"Error: {str(e)}"

# Set page config
st.set_page_config(
    page_title="LLM Debater 🚨"
)

# Custom CSS for debate layout
st.markdown("""
<style>
.pro-message {
    margin-right: 50%;
    padding: 10px;
    text-align: left;
}
.con-message {
    margin-left: 50%;
    padding: 10px;
    text-align: right;
}
.judge-message {
    margin: 20px auto;
    padding: 15px;
    background-color: #f0f2f6;
    border-radius: 5px;
    text-align: center;
}
.final-verdict {
    margin: 20px auto;
    padding: 20px;
    background-color: #1e1e1e;
    color: white;
    border-radius: 10px;
    text-align: center;
    font-weight: bold;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: 2px solid #4a4a4a;
}
.stMarkdown {
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("AI Debate Arena")

# User input section at the top
col1, col2 = st.columns([2,2])
with col1:
    model1 = st.selectbox("Select first debater model", ["llama2", "mistral", "neural-chat"], index=0)
with col2:
    model2 = st.selectbox("Select second debater model", ["llama2", "mistral", "neural-chat"], index=1)

col1, col2, col3 = st.columns([1,1,2])
with col1:
    rounds = st.number_input("Debate rounds", min_value=1, max_value=5, value=3, key="debate_rounds")
with col2:
    st.text('')
    st.text('')
    enable_scoring = st.checkbox("Enable Judging", value=True)
with col3:
    if enable_scoring:
        judge_model = st.selectbox("Select judge model", ["llama2", "mistral", "neural-chat"], index=2)

topic = st.text_input("Enter the topic for debate:")

# Initialize session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.current_round = 0
    st.session_state.scores = {"LLM1": 0, "LLM2": 0}

def display_message(content, is_pro=True, model="", is_judge=False):
    if is_judge:
        st.markdown(f'<div class="judge-message">⚖️ <strong>Judge ({model}):</strong> {content}</div>', unsafe_allow_html=True)
    elif is_pro:
        st.markdown(f'<div class="pro-message">🟦 <strong>Pro ({model}):</strong> {content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="con-message">🟥 <strong>Con ({model}):</strong> {content}</div>', unsafe_allow_html=True)

def get_judge_verdict(context, round_num):
    judge_prompt = f"""As an impartial judge, evaluate the last exchange in this debate about '{topic}':
    Pro: {context[-2]['content']}
    Con: {context[-1]['content']}

    Who made the more compelling argument in this round? Consider logic, evidence, and persuasiveness. Provide your scoring decision in exactly one sentence."""

    return get_llm_response(judge_prompt, judge_model)

def get_final_verdict(all_messages):
    debate_summary = "\n".join([f"{'Pro' if msg['role'] == 'LLM1' else 'Con'}: {msg['content']}" for msg in all_messages if msg['role'] != 'JUDGE'])

    final_prompt = f"""As an impartial judge, review this entire debate about '{topic}':
    {debate_summary}

    Based on the overall quality of arguments, logical reasoning, and persuasiveness, which side (Pro or Con) won the debate? Provide your final verdict in exactly one sentence."""

    return get_llm_response(final_prompt, judge_model)

if st.button("Start Debate"):
    if topic:
        # Clear previous debate
        st.session_state.messages = []
        st.session_state.current_round = 0
        st.session_state.scores = {"LLM1": 0, "LLM2": 0}

        # Opening statements
        llm1_prompt = f"You are participating in a debate. Give a compelling argument FOR this topic: {topic}"
        llm1_response = get_llm_response(llm1_prompt, model1)
        st.session_state.messages.append({"role": "LLM1", "content": llm1_response, "model": model1})
        display_message(llm1_response, True, model1)

        sleep(1)

        llm2_prompt = f"You are participating in a debate. Give a compelling argument AGAINST this topic: {topic}"
        llm2_response = get_llm_response(llm2_prompt, model2)
        st.session_state.messages.append({"role": "LLM2", "content": llm2_response, "model": model2})
        display_message(llm2_response, False, model2)

        # No per-round verdict after first round

        st.session_state.current_round = 1

        # Subsequent rounds
        for round in range(2, rounds + 1):
            sleep(1)

            # LLM1's turn
            last_opponent_msg = next((msg for msg in reversed(st.session_state.messages) if msg["role"] == "LLM2"), None)
            if last_opponent_msg:
                llm1_prompt = f"Your opponent argues: '{last_opponent_msg['content']}'. Directly address this point while defending the original position: {topic}"
            else:
                llm1_prompt = f"Provide an argument supporting this position: {topic}"
            llm1_response = get_llm_response(llm1_prompt, model1)
            st.session_state.messages.append({"role": "LLM1", "content": llm1_response, "model": model1})
            display_message(llm1_response, True, model1)

            sleep(1)

            # LLM2's turn
            last_opponent_msg = next((msg for msg in reversed(st.session_state.messages) if msg["role"] == "LLM1"), None)
            llm2_prompt = f"Your opponent argues: '{last_opponent_msg['content']}'. Directly address this point while arguing against the original position: {topic}"
            llm2_response = get_llm_response(llm2_prompt, model2)
            st.session_state.messages.append({"role": "LLM2", "content": llm2_response, "model": model2})
            display_message(llm2_response, False, model2)

            # Continue with debate without per-round verdicts

            st.session_state.current_round = round

        # Final verdict at the end of the debate
        if enable_scoring:
            sleep(1)
            final_verdict = get_final_verdict(st.session_state.messages)
            st.markdown(f'<div class="final-verdict">🏆 <strong>Final Verdict:</strong> {final_verdict}</div>', unsafe_allow_html=True)
