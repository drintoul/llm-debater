from time import sleep
from llm_service import LLMService

class DebateManager:
    def __init__(self, topic, model1, model2, judge_model=None, fact_checker_model=None):
        self.topic = topic
        self.model1 = model1  # Always Pro side
        self.model2 = model2  # Always Con side
        self.judge_model = judge_model
        self.fact_checker_model = fact_checker_model
        self.llm_service = LLMService()
        self.pro_wins = 0
        self.con_wins = 0
        self.rounds_tracked = 0  # Track number of rounds evaluated

    def get_pro_opening(self):
        pro_prompt = f"""You will now provide an argument FOR this statement: {self.topic}
        You are representing the PRO side of this debate. Provide your strongest single-sentence argument IN FAVOR of this statement.
        Make it concise but compelling, arguing that the statement is TRUE."""
        return self.llm_service.get_response(pro_prompt, self.model1)

    def get_con_opening(self):
        con_prompt = f"""You will now provide an argument AGAINST this statement: {self.topic}
        You are representing the CON side of this debate. Provide your strongest single-sentence argument AGAINST this statement.
        Make it concise but compelling, arguing that the statement is FALSE."""
        return self.llm_service.get_response(con_prompt, self.model2)

    def get_pro_argument(self, last_con_msg):
        pro_prompt = f"""You are on the PRO side of this debate about: '{self.topic}'
        Your opponent (CON side) just argued: '{last_con_msg}'
        Provide a single, strong counter-argument that SUPPORTS the original statement.
        Directly address your opponent's argument while maintaining your pro stance."""
        return self.llm_service.get_response(pro_prompt, self.model1)

    def get_con_argument(self, last_pro_msg):
        con_prompt = f"""You are on the CON side of this debate about: '{self.topic}'
        Your opponent (PRO side) just argued: '{last_pro_msg}'
        Provide a single, strong counter-argument that OPPOSES the original statement.
        Directly address your opponent's argument while maintaining your con stance."""
        return self.llm_service.get_response(con_prompt, self.model2)

    def fact_check_statement(self, statement):
        if not self.fact_checker_model:
            return None

        prompt = f"""Fact check this statement in one sentence.
        "{statement}"

        Your response MUST begin with exactly one of these labels (including the colon):
        VERIFIED: 
        PARTIALLY VERIFIED: 
        UNVERIFIED: 

        After the label, provide your fact check explanation. Example responses:
        VERIFIED: The statement accurately reflects historical data...
        PARTIALLY VERIFIED: While the basic premise is true, some details are inaccurate...
        UNVERIFIED: This claim lacks sufficient evidence..."""

        response = self.llm_service.get_response(prompt, self.fact_checker_model)

        # Validate and fix response format if needed
        if not any(response.startswith(label) for label in ["VERIFIED:", "PARTIALLY VERIFIED:", "UNVERIFIED:"]):
            # If no valid label, prepend UNVERIFIED as default
            response = "UNVERIFIED: " + response

        return response

    def evaluate_round(self, pro_arg, con_arg):
        if not self.judge_model:
            return None

        # Prevent scoring more rounds than specified
        if self.rounds_tracked >= 5:  # Assuming max 5 rounds
            return None

        prompt = f"""As an impartial judge, evaluate these arguments about '{self.topic}':
        Pro's argument (supporting the statement): {pro_arg}
        Con's argument (opposing the statement): {con_arg}

        Who won this round? Respond with exactly one of: PRO, CON, or TIE."""

        result = self.llm_service.get_response(prompt, self.judge_model)

        # Update scores based on round result
        if "PRO" in result.upper():
            self.pro_wins += 1
        elif "CON" in result.upper():
            self.con_wins += 1
        else:  # TIE case
            self.pro_wins += 0.5
            self.con_wins += 0.5

        self.rounds_tracked += 1
        return result

    def get_final_verdict(self, pro_final, con_final):
        if not self.judge_model:
            return None

        # Determine winner based on point totals
        final_score = f"({self.pro_wins} - {self.con_wins})"

        # Decide winner based on point totals
        if self.pro_wins > self.con_wins:
            verdict_start = f"Pro wins {final_score}"
            winner_side = "Pro"
            loser_side = "Con"
        elif self.con_wins > self.pro_wins:
            verdict_start = f"Con wins {final_score}"
            winner_side = "Con"
            loser_side = "Pro"
        else:
            verdict_start = f"The debate is a tie {final_score}"
            winner_side = None
            loser_side = None

        # Add reasoning from judge model
        if winner_side:
            # First get a concise summary of winning arguments
            summary_prompt = f"""Review the entire debate about '{self.topic}' and provide a two-sentence summary of why the {winner_side} side's arguments were most compelling. Focus only on their strongest points and most persuasive reasoning.

            Your response must be exactly two sentences, starting with "The {winner_side} side effectively argued that..."
            Do not reference debate points or scoring."""

            winning_summary = self.llm_service.get_response(summary_prompt, self.judge_model)

            # Then get the detailed analysis
            prompt = f"""As an impartial judge, analyze the entire debate about '{self.topic}'.
                Following this concise summary of the winning arguments:
                {winning_summary}

                Provide a comprehensive explanation for why the {winner_side} side was more persuasive.

                Your explanation should:
                1. Highlight the strongest and most compelling arguments made by the {winner_side} side
                2. Explain specific weaknesses in the {loser_side} side's argumentation
                3. Demonstrate how the {winner_side} side more effectively addressed the core issues of the debate
                4. Explain why the {winner_side} side's reasoning was ultimately more convincing

                Be specific, analytical, and provide clear reasoning that goes beyond simply counting points.

                Format your response starting with: "{verdict_start} because..."
                Do not simply reference that one side had more points.
                Provide a substantive, insightful analysis of the debate's outcome."""
        else:
            # For ties, get a balanced two-sentence summary
            summary_prompt = f"""Review the entire debate about '{self.topic}' and provide a two-sentence summary explaining why both sides presented equally compelling arguments. Focus on the key points that made this debate so balanced.

            Your response must be exactly two sentences, starting with "Both sides presented compelling arguments, with..."
            Do not reference debate points or scoring."""

            tie_summary = self.llm_service.get_response(summary_prompt, self.judge_model)

            prompt = f"""As an impartial judge, analyze the entire debate about '{self.topic}'.
                Following this concise summary of the balanced arguments:
                {tie_summary}

                Provide a comprehensive explanation for why the debate resulted in a tie.

                Your explanation should:
                1. Highlight the equally strong arguments from both sides
                2. Explain how both Pro and Con sides presented equally compelling points
                3. Discuss the nuanced and balanced nature of the debate topic
                4. Demonstrate why neither side could definitively prove their position

                Be specific, analytical, and provide clear reasoning for the tie.

                Format your response starting with: "{verdict_start} because..."
                Provide a substantive, nuanced analysis of the debate's balanced outcome."""

        # Get judge's reasoning
        judge_reasoning = self.llm_service.get_response(prompt, self.judge_model)

        # Ensure the verdict matches the actual score
        if not judge_reasoning.lower().startswith(verdict_start.lower()):
            # If judge's response doesn't match score, construct a generic response
            judge_reasoning = f"{verdict_start} because the arguments presented were carefully evaluated, revealing the complexity of the debate topic."

        return judge_reasoning
