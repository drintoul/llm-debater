import random
import streamlit as st
from config import AVAILABLE_MODELS, MAX_ROUNDS, DEFAULT_ROUNDS, MODEL_CUTOFF_DATES, OLLAMA_HOST
from llm_service import LLMService

class DebateUI:
    @staticmethod
    def format_score(score):
        """
        Convert decimal scores to use ½ symbol.
        Examples:
        0.5 → ½
        2.5 → 2½
        1.0 → 1
        2.0 - 1.5 → 2 - 1½
        """
        # Special case for 0.5
        if score == 0.5:
            return '½'

        # Convert to string and replace .5 with ½ and .0 with empty string
        formatted = str(score).replace('.5', '½').replace('.0', '')

        return formatted

    @staticmethod
    @st.cache_data(ttl=10)
    def _ping_server():
        """Ping the Ollama server (cached 10s so reruns don't hammer it)."""
        return LLMService.check_server_health()

    @staticmethod
    @st.cache_data(ttl=30)
    def _pulled_models():
        """Fetch pulled model names from the server (cached 30s)."""
        return LLMService.get_pulled_models()

    @staticmethod
    def check_server_status():
        """Check if the Ollama server is available and display status"""
        server_status = DebateUI._ping_server()

        if not server_status:
            st.sidebar.error(f"""⚠️ Ollama Server Offline

            Cannot connect to {OLLAMA_HOST}

            Please ensure:
            - Ollama is running and accessible
            - OLLAMA_HOST is set correctly
            - Required models are installed""")
        else:
            # Warn early if a configured model isn't actually pulled on the server
            pulled = DebateUI._pulled_models()
            if pulled is not None:
                missing = [m for m in AVAILABLE_MODELS
                           if m not in pulled and f"{m}:latest" not in pulled]
                if missing:
                    st.sidebar.warning(
                        f"""⚠️ Not pulled on the Ollama server: {', '.join(missing)}

                        Run `ollama pull <model>` on the server, or remove it from AVAILABLE_MODELS.""")

        return server_status

    @staticmethod
    def render_controls():
        # Check server status immediately on startup
        server_online = DebateUI.check_server_status()

        # Move configuration controls to sidebar
        with st.sidebar:
            st.header("Debate Configuration")
            st.caption("Two models debate a topic — one argues Pro, the other argues Con.")

            # Random defaults, keeping Pro / Con / Judge distinct.
            # Roll once per session and store — re-rolling each rerun would
            # reshuffle the other dropdowns whenever a widget changes.
            if "model_picks" not in st.session_state:
                st.session_state.model_picks = random.sample(
                    range(len(AVAILABLE_MODELS)), min(4, len(AVAILABLE_MODELS))
                )
            picks = st.session_state.model_picks

            model1 = st.selectbox(
                "Pro model",
                AVAILABLE_MODELS,
                index=picks[0],
                help="This model argues in favor of the topic statement."
            )
            model2 = st.selectbox(
                "Con model",
                AVAILABLE_MODELS,
                index=picks[1],
                help="This model argues against the topic statement."
            )
            rounds = st.selectbox(
                "Number of Rounds",
                options=list(range(1, MAX_ROUNDS + 1)),
                index=DEFAULT_ROUNDS - 1,
                help="Round 1 is opening statements. In each later round, both debaters respond to the other's last argument."
            )

            st.subheader("Additional Features")
            response_length = st.selectbox(
                "Argument length",
                ["One sentence", "Short paragraph"],
                index=0,
                help="One sentence keeps debates terse and fast; a short paragraph (3-4 sentences) allows deeper arguments but slower turns."
            )
            enable_scoring = st.checkbox(
                "Enable Judging",
                value=True,
                help="A judge model scores every round (Pro / Con / Tie) and writes a final verdict explaining the outcome."
            )
            judge_model = None
            if enable_scoring:
                judge_model = st.selectbox(
                    "Judge model",
                    AVAILABLE_MODELS,
                    index=picks[2] if len(picks) > 2 else 0,
                    help="Evaluates each exchange impartially. A larger model usually judges more reliably."
                )

            enable_fact_checking = st.checkbox(
                "Enable Fact Checking",
                value=False,
                help="After every statement, the fact-checker model labels it VERIFIED, PARTIALLY VERIFIED, or UNVERIFIED."
            )
            fact_checker_model = None
            if enable_fact_checking:
                fact_checker_model = st.selectbox(
                    "Fact checker model",
                    AVAILABLE_MODELS,
                    index=picks[3] if len(picks) > 3 else picks[0],
                    help="Reviews each debater's claim against its training knowledge. Checks are limited to what the model itself knows."
                )

            if enable_scoring or enable_fact_checking:
                st.caption("Note: judging and fact checking add extra model calls, so debates run slower.")

            # Add model training cutoff dates at bottom of sidebar
            st.markdown("---")
            with st.expander("Model Training Cutoff Dates"):
                cutoff_table = "<small>" + "<br>".join([f"{model}: {MODEL_CUTOFF_DATES.get(model, 'unknown')}" for model in sorted(AVAILABLE_MODELS)]) + "</small>"
                st.markdown(cutoff_table, unsafe_allow_html=True)

        # Add instructions in main area
        with st.expander("How to Use"):
            st.markdown("""
            1. **Configure Your Debate** (using sidebar):
               - Choose AI models for both debaters
               - Set the number of debate rounds
               - Enable optional judging and fact-checking

            2. **Enter Your Topic** below:
               - Make it clear and specific
               - Phrase it as a statement that can be debated

            3. **Start the Debate**:
               - Click the 'Start Debate' button
               - Watch the AI models argue turn by turn — arguments stream in live
               - Follow the discussion through multiple rounds
               - Download the transcript afterwards if you want to keep it
            """)

        with st.expander("About This Arena"):
            st.markdown("""
            **How it works:** Round 1 is opening statements; in later rounds each debater sees the
            transcript and counters its opponent's last point. The optional judge scores each round
            with a one-sentence reason and writes a final verdict. The optional fact-checker labels
            each claim VERIFIED, PARTIALLY VERIFIED, or UNVERIFIED.

            **Why it's interesting:** it's a sandbox for comparing model behavior under identical
            prompts — persuasiveness, consistency, and failure modes like repetition and confident
            hallucination — all running locally and privately on your own Ollama server.

            **Limitations & caution:** arguments are intentionally short (one sentence or a
            brief paragraph); "fact checks" only reflect the checker's own training data
            (nothing is looked up); judge scores are inconsistent and can't verify claims.
            This is a demo — don't rely on the outputs for real decisions or use it in production.
            """)

        # Initialize default topic in session state if not present
        if "topic_content" not in st.session_state:
            st.session_state.topic_content = "Cats make better pets than dogs."

        # Topic input and clear button in the same column layout
        col1, col2 = st.columns([4, 1])  # 4:1 ratio to make text area wider than button

        # Handle clear button click before creating text area
        with col2:
            st.write("")
            if st.button("Clear", type="secondary", key="clear_button"):
                # Reset the topic content in session state
                st.session_state.topic_content = ""
                # Explicitly set the key to force re-render
                st.session_state.topic_input_unique = "clear_" + str(st.session_state.get('topic_clear_counter', 0))
                st.session_state.topic_clear_counter = st.session_state.get('topic_clear_counter', 0) + 1
                # Also clear any previous messages or debate state
                st.session_state.pop("messages", None)
                st.session_state.pop("debate_log", None)
                st.rerun()

        with col1:
            # Use dynamic key to force re-render when cleared
            topic = st.text_area(
                "Enter the topic for debate:",
                height=100,
                value=st.session_state.topic_content,
                key=st.session_state.get('topic_input_unique', 'topic_input_default')
            )

        return topic, model1, model2, rounds, response_length, enable_scoring, judge_model, enable_fact_checking, fact_checker_model, server_online

    @staticmethod
    def _bubble_html(content, is_pro, model):
        message_class = "pro-message" if is_pro else "con-message"
        side = "Pro" if is_pro else "Con"
        side_color = "#0066cc" if is_pro else "#cc0000"
        return f'<div class="{message_class}"><strong style="color: {side_color};">{side} ({model}):</strong> {content}</div>'

    @staticmethod
    def display_message(content, is_pro=True, model="", fact_check=None):
        st.markdown(DebateUI._bubble_html(content, is_pro, model), unsafe_allow_html=True)
        if fact_check:
            DebateUI.display_fact_check(fact_check, is_pro)

    @staticmethod
    def stream_message(token_stream, is_pro=True, model=""):
        """Render a debater's response into its bubble as tokens arrive.

        Shows a 'thinking' placeholder until the first token, then re-renders
        the bubble with accumulated text. Returns the full raw response text.
        """
        side = "Pro" if is_pro else "Con"
        placeholder = st.empty()
        placeholder.markdown(DebateUI._bubble_html("<em>thinking…</em>", is_pro, model), unsafe_allow_html=True)

        text = ""
        for token in token_stream:
            text += token
            placeholder.markdown(DebateUI._bubble_html(text, is_pro, model), unsafe_allow_html=True)

        return text

    @staticmethod
    def display_fact_check(fact_check, is_pro=True):
        # Strip markdown and formatting
        cleaned_text = (fact_check.replace("🔍", "")
                     .replace("**Fact Check:**", "")
                     .replace("*", "")
                     .strip())

        # Extract just the label part (everything before the first actual content)
        label_part = cleaned_text.split(":")[0] + ":" if ":" in cleaned_text else ""

        # Determine the CSS class based on the exact label
        if label_part.upper() == "VERIFIED:":
            fact_check_class = "fact-check-verified"
        elif label_part.upper() == "PARTIALLY VERIFIED:":
            fact_check_class = "fact-check-partial"
        else:
            fact_check_class = "fact-check-unverified"

        # Align the fact-check box with its message bubble (Pro left / Con right)
        fc_style = "" if is_pro else "margin-left: auto; margin-right: 0;"

        st.markdown(f'''
        <div class="fact-check {fact_check_class}" style="{fc_style}">
            🔍 <strong>Fact Check:</strong> {cleaned_text}
        </div>
        ''', unsafe_allow_html=True)

    @staticmethod
    def display_verdict(verdict):
        if not verdict:
            return
        if verdict.startswith("Error:"):
            st.error(verdict)
            return

        verdict_lower = verdict.lower().strip()
        verdict_class = "verdict-tie"
        outcome = "TIE"

        # Extract score from verdict text (assuming format like "(2 - 1)")
        # so it can be stripped — the round scoreboard already shows it
        score = ""
        if "(" in verdict and ")" in verdict:
            score = verdict[verdict.find("("): verdict.find(")") + 1]

        # Clean verdict text to remove score, and strip any markdown the model
        # emitted — it renders literally inside the HTML div below
        verdict_text = verdict.replace(score, "").strip()
        for token in ("**", "__", "###", "##", "#"):
            verdict_text = verdict_text.replace(token, "")

        # Extract and format the two-sentence summary
        summary = ""
        explanation = verdict_text

        # Look for the summary in the response (it will be the first two sentences)
        sentences = verdict_text.split('. ')
        if len(sentences) >= 2:
            summary = '. '.join(sentences[:2]) + '.'
            explanation = '. '.join(sentences[2:]).strip()
            if explanation.startswith(' because'):
                explanation = explanation[8:].strip()  # Remove 'because' from the start

        # Adjust outcome and verdict class based on text
        if "pro wins" in verdict_lower:
            verdict_class = "verdict-pro"
            outcome = "PRO WINS"
        elif "con wins" in verdict_lower:
            verdict_class = "verdict-con"
            outcome = "CON WINS"

        final_classes = f"final-verdict {verdict_class}"

        # Add the explicit outcome followed by the explanation
        st.markdown(
            f'''<div class="{final_classes}">
                <div class="verdict-outcome">🏆 {outcome}</div>
                <div class="verdict-summary">{summary}</div>
                <div class="verdict-explanation">{explanation}</div>
             </div>''',
            unsafe_allow_html=True
        )
