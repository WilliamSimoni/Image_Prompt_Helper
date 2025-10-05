from src.image_prompt_helper import PromptGenerator
from src.image_prompt_helper.utils import get_lm

lm = get_lm()

initial_prompt = input("Write your prompt for the image you want to generate: ")
initial_hint = input("Do you have focus on any specific aspect? (e.g., style, color, mood, composition) If not, just press enter: ")

## -- First step
prompt_generator = PromptGenerator(lm=lm)
prompts = prompt_generator(user_image_prompt=initial_prompt, user_feedback=initial_hint)

## -- Refinement step
MAX_ITERATIONS = 100
iteration = 0

while iteration < MAX_ITERATIONS:
    print("="*20)

    if len(prompts) == 0:
        print("No prompts generated. Exiting.")
        break

    prompt = prompts[0]
    print(f"Prompt: {prompt}")

    user_input = input("Are you satisfied with this prompt or do you want to refine? (s/r): ")

    if user_input.lower() == 'r':
        feedback = input("Please provide your feedback on the prompt: ")
        prompts = prompt_generator(user_image_prompt=prompt, user_feedback=feedback)
        iteration += 1
    elif user_input.lower() == 's':
        print("Completed")
        break
    else:
        print("Invalid input. Please enter 's' to stop or 'r' to refine.")
        continue