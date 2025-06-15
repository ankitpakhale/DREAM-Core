from typing import Dict, Any
from .base_generator import BaseGenerator
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from app.utils import logger
from app.clients import GroqAIClient
from app.prompts import prompt_factory
from app.utils.constants import PROMPT_TYPE, PROMPT_CATEGORY, PAYLOAD_CATEGORY
import json
import os
from app.services.validation_manager import ValidationManager
from app.utils import retry
from app.config import GeneralConfig


# ------------------------------
# Domain model for FearAndMotivation Generator response
# ------------------------------
class FearDoubtContent(BaseModel):
    """Model for content related to mindset shift, motivation, and perspective for each fear or doubt."""

    mindset_shift: str
    motivation: str
    perspective: str


class FinalMotivation(BaseModel):
    """Model for the final motivation section with motivation, remembering 'why', and believing in ability to adapt."""

    motivation: str
    remember_your_why: str
    believe_in_your_ability_to_adapt: str


class MindsetMessages(BaseModel):
    """Model for various fears, doubts, and motivational messages to shift mindset and keep the reader focused."""

    fear_of_not_making_significant_impact: FearDoubtContent
    fear_of_burnout: FearDoubtContent
    doubt_about_achieving_financial_freedom: FearDoubtContent
    doubt_about_successfully_scaling_investment_portfolio: FearDoubtContent
    final_motivation_to_push_through: FinalMotivation


# ------------------------------
# FearAndMotivation Generator
# ------------------------------
class FearAndMotivationGenerator(BaseGenerator):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(FearAndMotivationGenerator, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    @staticmethod
    def _validate(
        payload: Dict[str, Any],
        payload_type: str = PAYLOAD_CATEGORY.FEAR_AND_MOTIVATION_GENERATOR_DATA,
    ) -> None:
        ValidationManager(validation_type=payload_type).validate(payload)

    @retry(max_retries=GeneralConfig.RETRY_COUNT, delay=1, backoff=2)
    async def generate(self, payload: Dict[str, Any]) -> Any:
        # load the output-schema for system prompt from JSON file
        parent_path = os.path.dirname(__file__).split("/")[:-2]
        relative_schema_path = ["schema", "fears_and_motivation_schema.json"]
        parent_path.extend(relative_schema_path)
        schema_path = "/".join(parent_path)

        with open(schema_path, "r", encoding="utf-8") as f:
            output_schema = json.load(f)

        # system prompt
        system_prompt = prompt_factory.build_prompt(
            prompt_type=PROMPT_TYPE.SYSTEM_PROMPT,
            prompt_category=PROMPT_CATEGORY.FEAR_AND_MOTIVATION_GENERATOR,
            schema={"OUTPUT_FORMAT": output_schema},
        )

        # user prompt
        user_prompt = prompt_factory.build_prompt(
            prompt_type=PROMPT_TYPE.USER_PROMPT,
            prompt_category=PROMPT_CATEGORY.FEAR_AND_MOTIVATION_GENERATOR,
            schema={"USER_DATA": payload},
        )

        raw_output = await GroqAIClient.get_response(
            system_prompt=system_prompt, user_prompt=user_prompt
        )

        # parse the output using the PydanticOutputParser
        output_parser = PydanticOutputParser(pydantic_object=MindsetMessages)
        parsed_result = output_parser.parse(raw_output)
        result = parsed_result.model_dump()
        logger.debug("result: %s", result)

        # validate the parsed result
        self._validate(
            payload=result,
            payload_type=PAYLOAD_CATEGORY.FEAR_AND_MOTIVATION_GENERATOR_DATA,
        )
        return result


# singleton instance of FearAndMotivationGenerator
fear_and_motivation_generator = FearAndMotivationGenerator()
