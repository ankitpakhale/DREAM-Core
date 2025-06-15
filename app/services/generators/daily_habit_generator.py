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
# Domain model for DailyHabit Generator response
# ------------------------------
class HabitContent(BaseModel):
    """Model for content related to 'why it's powerful', 'what to do', and 'long term impact'."""

    why_its_powerful: str
    what_to_do: str
    long_term_impact: str


class TheBigPicture(BaseModel):
    """Model for the 'big picture' summary and reminder."""

    summary: str
    reminder: str


class DailyHabits(BaseModel):
    """Model for various daily habits, including morning mindset, focused learning, investment tracking, etc."""

    morning_mindset_ritual: HabitContent
    focused_learning: HabitContent
    daily_investment_tracking: HabitContent
    relationship_building: HabitContent
    daily_reflection_and_goal_review: HabitContent
    the_big_picture: TheBigPicture


# ------------------------------
# DailyHabit Generator
# ------------------------------
class DailyHabitGenerator(BaseGenerator):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DailyHabitGenerator, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    @staticmethod
    def _validate(
        payload: Dict[str, Any],
        payload_type: str = PAYLOAD_CATEGORY.DAILY_HABIT_GENERATOR_DATA,
    ) -> None:
        ValidationManager(validation_type=payload_type).validate(payload)

    @retry(max_retries=GeneralConfig.RETRY_COUNT, delay=1, backoff=2)
    async def generate(self, payload: Dict[str, Any]) -> Any:
        # load the output-schema for system prompt from JSON file
        parent_path = os.path.dirname(__file__).split("/")[:-2]
        relative_schema_path = ["schema", "daily_habits_schema.json"]
        parent_path.extend(relative_schema_path)
        schema_path = "/".join(parent_path)

        with open(schema_path, "r", encoding="utf-8") as f:
            output_schema = json.load(f)

        system_prompt = prompt_factory.build_prompt(
            prompt_type=PROMPT_TYPE.SYSTEM_PROMPT,
            prompt_category=PROMPT_CATEGORY.DAILY_HABIT_GENERATOR,
            schema={"OUTPUT_FORMAT": output_schema},
        )

        user_prompt = prompt_factory.build_prompt(
            prompt_type=PROMPT_TYPE.USER_PROMPT,
            prompt_category=PROMPT_CATEGORY.DAILY_HABIT_GENERATOR,
            schema={"USER_DATA": payload},
        )

        raw_output = await GroqAIClient.get_response(
            system_prompt=system_prompt, user_prompt=user_prompt
        )

        # parse the output using the PydanticOutputParser
        output_parser = PydanticOutputParser(pydantic_object=DailyHabits)
        parsed_result = output_parser.parse(raw_output)
        result = parsed_result.model_dump()
        logger.debug("result: %s", result)

        # validate the parsed result
        self._validate(
            payload=result, payload_type=PAYLOAD_CATEGORY.DAILY_HABIT_GENERATOR_DATA
        )
        print(f"==>> result: {result}")
        return result


# singleton instance of DailyHabitGenerator
daily_habit_generator = DailyHabitGenerator()
