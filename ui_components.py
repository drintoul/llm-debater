import streamlit as st
from config import AVAILABLE_MODELS, MAX_ROUNDS, DEFAULT_ROUNDS

class DebateUI:
    @staticmethod
    def render_controls():
        # Move configuration controls to sidebar
        with st.sidebar:
            st.header("Debate Configuration")

            st.subheader("Debater Models")
            model1 = st.selectbox("First debater model", AVAILABLE_MODELS, index=0)
            model2 = st.selectbox("Second debater model", AVAILABLE_MODELS, index=1)

            st.subheader("Debate Settings")
            rounds = st.number_input("Number of rounds", min_value=1, max_value=MAX_ROUNDS, value=DEFAULT_ROUNDS)

            st.subheader("Additional Features")
            enable_scoring = st.checkbox("Enable Judging", value=True)
            judge_model = None
            if enable_scoring:
                judge_model = st.selectbox("Judge model", AVAILABLE_MODELS, index=2)

            enable_fact_checking = st.checkbox("Enable Fact Checking", value=False)
            fact_checker_model = None
            if enable_fact_checking:
                fact_checker_model = st.selectbox("Fact checker model", AVAILABLE_MODELS, index=2)

        # Add instructions in main area
        st.markdown("""
        ### How to Use the AI Debate Arena

        1. **Configure Your Debate** (using sidebar):
           - Choose AI models for both debaters
           - Set the number of debate rounds
           - Enable optional judging and fact-checking

        2. **Enter Your Topic** below:
           - Make it clear and specific
           - Phrase it as a statement that can be debated
           - Example: "Social media has a net positive impact on society"

        3. **Start the Debate**:
           - Click the 'Start Debate' button
           - Watch as the AI models engage in real-time debate
           - Follow the discussion through multiple rounds
        """)

        # Topic input
        topic = st.text_area("Enter the topic for debate:", height=3, key="debate_topic")

        return topic, model1, model2, rounds, enable_scoring, judge_model, enable_fact_checking, fact_checker_model

    @staticmethod
    def display_message(content, is_pro=True, model="", is_judge=False, fact_check=None):
        if is_judge:
            st.markdown(f'<div class="judge-message">⚖️ <strong>Judge ({model}):</strong> {content}</div>', unsafe_allow_html=True)
        else:
            message_class = "pro-message" if is_pro else "con-message"
            icon = "🟦" if is_pro else "🟥"
            side = "Pro" if is_pro else "Con"

            st.markdown(f'<div class="{message_class}">{icon} <strong>{side} ({model}):</strong> {content}</div>', unsafe_allow_html=True)

            if fact_check:
                # Strip markdown and formatting
                cleaned_text = (fact_check.replace("🔍", "")
                             .replace("**Fact Check:**", "")
                             .replace("*", "")
                             .strip())

                # Log the cleaned text for debugging
                print(f"Cleaned fact check text: '{cleaned_text}'")

                # Extract just the label part (everything before the first actual content)
                label_part = cleaned_text.split(":")[0] + ":" if ":" in cleaned_text else ""
                print(f"Extracted label: '{label_part}'")

                # Determine the CSS class based on the exact label
                if label_part.upper() == "VERIFIED:":
                    fact_check_class = "fact-check-verified"
                elif label_part.upper() == "PARTIALLY VERIFIED:":
                    fact_check_class = "fact-check-partial"
                elif label_part.upper() == "UNVERIFIED:":
                    fact_check_class = "fact-check-unverified"
                else:
                    fact_check_class = "fact-check-unverified"  # default case

                print(f"Selected class: {fact_check_class}")

                # Create div with both base and specific classes
                html = f'''
                <div class="fact-check {fact_check_class}" style="margin-top: 5px; padding: 10px; border-radius: 5px;">
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
                <div class="verdict-outcome">🏆 <strong>{outcome}</strong></div>
                <div class="verdict-explanation">{verdict}</div>
             </div>''',
            unsafe_allow_html=True
        )
