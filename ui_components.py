import streamlit as st
import logging
from config import AVAILABLE_MODELS, MAX_ROUNDS, DEFAULT_ROUNDS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    def render_controls():
        # Move configuration controls to sidebar
        with st.sidebar:
            st.header("Debate Configuration")

            st.subheader("Debater Models")
            model1 = st.selectbox("First debater model", AVAILABLE_MODELS, index=0)
            model2 = st.selectbox("Second debater model", AVAILABLE_MODELS, index=0)

            st.subheader("Debate Settings")
            rounds = st.number_input("Number of rounds", min_value=1, max_value=MAX_ROUNDS, value=DEFAULT_ROUNDS)

            st.subheader("Additional Features")
            enable_scoring = st.checkbox("Enable Judging", value=True)
            judge_model = None
            if enable_scoring:
                judge_model = st.selectbox("Judge model", AVAILABLE_MODELS, index=0)

            enable_fact_checking = st.checkbox("Enable Fact Checking", value=False)
            fact_checker_model = None
            if enable_fact_checking:
                fact_checker_model = st.selectbox("Fact checker model", AVAILABLE_MODELS, index=0)

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
               - Watch as the AI models engage in real-time debate
               - Follow the discussion through multiple rounds
            """)

        # Initialize default topic in session state if not present
        if "topic_content" not in st.session_state:
            st.session_state.topic_content = "Social media has a net positive impact on society"

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
                if "messages" in st.session_state:
                    del st.session_state.messages
                if "current_round" in st.session_state:
                    del st.session_state.current_round
                st.rerun()

        with col1:
            # Use dynamic key to force re-render when cleared
            topic = st.text_area(
                "Enter the topic for debate:",
                height=3,
                value=st.session_state.topic_content,
                key=st.session_state.get('topic_input_unique', 'topic_input_default')
            )

        return topic, model1, model2, rounds, enable_scoring, judge_model, enable_fact_checking, fact_checker_model

    @staticmethod
    def display_message(content, is_pro=True, model="", is_judge=False, fact_check=None):
        # Log the side assignment for debugging
        logger.info(f"Displaying message: is_pro={is_pro}, model={model}")

        if is_judge:
            st.markdown(f'<div class="judge-message">⚖️ <strong>Judge ({model}):</strong> {content}</div>', unsafe_allow_html=True)
        else:
            message_class = "pro-message" if is_pro else "con-message"
            side = "Pro" if is_pro else "Con"
            side_color = 'style="color: #0066cc;"' if is_pro else 'style="color: #cc0000;"'

            st.markdown(f'<div class="{message_class}"><strong {side_color}>{side} ({model}):</strong> {content}</div>', unsafe_allow_html=True)

            if fact_check:
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
                elif label_part.upper() == "UNVERIFIED:":
                    fact_check_class = "fact-check-unverified"
                else:
                    fact_check_class = "fact-check-unverified"  # default case

                # Create div with both base and specific classes
                html = f'''
                <div class="fact-check {fact_check_class}">
                    🔍 <strong>Fact Check:</strong> {cleaned_text}
                </div>
                '''

                st.markdown(html, unsafe_allow_html=True)

    @staticmethod
    def display_verdict(verdict):
        if not verdict:
            return

        verdict_lower = verdict.lower().strip()
        verdict_class = "verdict-tie"
        outcome = "TIE"

        # Extract score from verdict (assuming format like "(2 - 1)")
        score = ""
        if "(" in verdict and ")" in verdict:
            score = verdict[verdict.find("("): verdict.find(")") + 1]
            # Convert score format from (2.5 - 1.5) to (2½ - 1½)
            score_parts = score.strip("()").split(" - ")
            if len(score_parts) == 2:
                # Convert decimal points to ½ symbol
                score_parts_formatted = [
                    DebateUI.format_score(float(part)) for part in score_parts
                ]
                score_html = f'''<div class="round-score" style="margin-bottom: 20px;">
                    <span class="score-pro">Pro {score_parts_formatted[0]}</span>
                    <span class="score-divider">-</span>
                    <span class="score-con">{score_parts_formatted[1]} Con</span>
                </div>'''
            else:
                score_html = ""  # In case score format is unexpected
        else:
            score_html = ""

        # Clean verdict text to remove score and create explanation
        verdict_text = verdict.replace(score, "").strip()

        # More robust explanation extraction
        explanation = verdict_text

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
                {score_html}
                <div class="verdict-explanation">{explanation}</div>
             </div>''',
            unsafe_allow_html=True
        )
