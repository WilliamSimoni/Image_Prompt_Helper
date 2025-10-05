import dspy
import os
import dotenv
import logging

dotenv.load_dotenv(override=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_lm():
    model = os.getenv("MODEL")
    api_base = os.getenv("API_BASE")
    api_key = os.getenv("API_KEY")
    max_tokens = int(os.getenv("MAX_TOKENS"))
    temperature = float(os.getenv("TEMPERATURE"))
    num_retries = int(os.getenv("NUM_RETRIES"))
    lm = dspy.LM(
        model=model,
        api_base=api_base,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=temperature,
        num_retries=num_retries,
    )
    logger.info(
        "Loading language model with the following parameters: model=%s, api_base=%s, max_tokens=%d, temperature=%.2f, num_retries=%d",
        model,
        api_base,
        max_tokens,
        temperature,
        num_retries,
    )
    return lm
