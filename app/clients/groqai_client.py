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
    sample_payload = {
        "having_nightmares": False,
        "having_trouble_with_work": True,
        "avoids_people_or_activities": False,
        "feeling_negative": False,
        "suicidal_thought": False,
        "trouble_concentrating": True,
        "hopelessness": False,
        "social_media_addiction": False,
        "anger": False,
        "feeling_tired": True,
        "trouble_in_concentration": False,
        "close_friend": False,
        "having_trouble_in_sleeping": True,
        "panic": True,
        "popping_up_stressful_memory": False,
        "over_react": True,
        "feeling_nervous": True,
        "introvert": True,
        "change_in_eating": False,
        "blamming_yourself": False,
        "weight_gain": False,
        "sweating": False,
        "breathing_rapidly": True,
        "material_possessions": False,
        "thoughts_summary": "I'm experiencing heightened anxiety and a sense of hopelessness. I'm struggling to sleep and concentrate, and I often have intrusive memories that trigger panic. I've had suicidal thoughts and feel like I'm blaming myself. I've noticed changes in my eating habits and weight gain, which may be linked to emotional eating due to stress. I feel nervous and tired, and I tend to overreact to situations, but I remain an introvert.",
    }

    client = GroqAIClient(sample_payload)
    result = client.generate_diagnosis()
    logger.info("Final diagnosis prediction:")
    logger.debug(json.dumps(result, indent=4))
