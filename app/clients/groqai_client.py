import json
from typing import Dict, Any

from app.utils import logger
from app.config import GroqAIConfig  # now using Groq configuration

from groq import Groq  # Import Groq client


# ------------------------------
# Client class for diagnosis prediction using Groq
# ------------------------------
class GroqAIClient:
    @staticmethod
    def get_response(system_prompt: str, user_prompt: str) -> Dict[str, Any]:

        # prepare the messages for the Groq chat completions API
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # instantiate the Groq client using API key from GroqAIConfig
        groq_client = Groq(api_key=GroqAIConfig.GROQ_API_KEY)

        # call the Groq chat completions API with parameters from the configuration
        completion = groq_client.chat.completions.create(
            model=GroqAIConfig.GROQ_MODEL,
            messages=messages,
            temperature=GroqAIConfig.GROQ_TEMPERATURE,
            max_completion_tokens=GroqAIConfig.GROQ_MAX_COMPLETION_TOKENS,
            top_p=GroqAIConfig.GROQ_TOP_P,
            stream=False,  # Using non-stream mode for a complete response
            stop=None,
        )
        raw_output = completion.choices[0].message.content
        logger.debug("Raw output from Groq: %s", raw_output)
        return raw_output


# FIXME: Fix this entry point
if __name__ == "__main__":
    sample_payload = {}

    client = GroqAIClient(sample_payload)
    result = client.get_response()
    logger.info("Final Prediction:")
    logger.debug(json.dumps(result, indent=4))
