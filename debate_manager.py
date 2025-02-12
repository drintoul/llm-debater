from time import sleep
from llm_service import LLMService

class DebateManager:
    def __init__(self, topic, model1, model2, judge_model=None, fact_checker_model=None):
        self.topic = topic
        self.model1 = model1
        self.model2 = model2
        self.judge_model = judge_model
        self.fact_checker_model = fact_checker_model
        self.llm_service = LLMService()

    def get_pro_opening(self):
        pro_prompt = f"""You are participating in a debate. Provide your strongest single-sentence argument FOR this topic: {self.topic}
        Make it concise but compelling."""
        return self.llm_service.get_response(pro_prompt, self.model1)

    def get_con_opening(self):
        con_prompt = f"""You are participating in a debate. Provide your strongest single-sentence argument AGAINST this topic: {self.topic}
        Make it concise but compelling."""
        return self.llm_service.get_response(con_prompt, self.model2)

    def get_pro_argument(self, last_con_msg):
        pro_prompt = f"""Your opponent argues: '{last_con_msg}'
        Provide a single, strong counter-argument sentence defending your position on: {self.topic}"""
        return self.llm_service.get_response(pro_prompt, self.model1)

    def get_con_argument(self, last_pro_msg):
        con_prompt = f"""Your opponent argues: '{last_pro_msg}'
        Provide a single, strong counter-argument sentence against: {self.topic}"""
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

    def get_final_verdict(self, pro_final, con_final):
        if not self.judge_model:
            return None

        prompt = f"""As an impartial judge, evaluate these final arguments about '{self.topic}':
        Pro's final argument: {pro_final}
        Con's final argument: {con_final}

        Provide a single-sentence verdict starting with exactly one of these:
        - "Pro wins because..."
        - "Con wins because..."
        - "The debate is a tie because..."
        """

        return self.llm_service.get_response(prompt, self.judge_model)
