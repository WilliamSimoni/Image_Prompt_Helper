import dspy

from typing import Callable, List, Tuple

def default_ask_questions(questions:str) -> List[str]:
    """use this tool to to get more context about the image you want to generate. Ask about relevant information. Use this tool until you have enough information to generate a good image prompt.

    Args:
        questions (str): questions to ask the user to get more context about the image they want to generate. Include suggestions for answers. Separate each question with a newline.
    Returns:
        List[str]: Questions and corresponding answers formatted as Q&A pairs.
    """
    answers = []
    for question in questions.split("\n"):
        question = question.strip()
        if not question:
            continue
        answer = input("Q: " + question + "\n=>")
        answers.append(f"Q: {question}\nA: {answer}")
    return answers    

class PromptGeneratorSignature(dspy.Signature):
    previous_prompt: str = dspy.InputField()
    user_feedback_on_prompt: str = dspy.InputField()
    questions_answers_summary: str = dspy.OutputField(desc="summary of information gathered from the user to generate a better image prompt")

class PromptGenerator(dspy.Module):
    
    def __init__(self, lm: dspy.LM, ask_questions: Callable[[str], List[str]] = default_ask_questions):
        super().__init__()
        self._lm = lm
        self.react_agent = dspy.ReAct(PromptGeneratorSignature, max_iters=3, tools=[ask_questions])
        self.generate_prompts = dspy.ChainOfThought("user_image_prompt:str, questions_and_answers:str -> new_image_prompt:str")

    def forward(self, user_image_prompt: str, user_feedback:str = "") -> List[str]:
        with dspy.context(lm=self._lm):
            react_agent_result =  self.react_agent(previous_prompt=user_image_prompt, user_feedback_on_prompt=user_feedback)
            prompt = self.generate_prompts(user_image_prompt=user_image_prompt, questions_and_answers=react_agent_result.questions_answers_summary)
            return [prompt.new_image_prompt]