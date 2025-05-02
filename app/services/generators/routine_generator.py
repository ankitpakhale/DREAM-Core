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

# ------------------------------
# Domain model for Routine Generator response
# ------------------------------


# ==== Career Routine Models ====
class CareerRoutineSteps(BaseModel):
    """Daily career actions like learning and deep work."""

    morning_routine: str
    deep_work: str
    team_engagement: str
    self_reflection: str


class CareerWeeklySteps(BaseModel):
    """Weekly career development actions."""

    strategy_review: str
    team_development: str
    networking: str
    growth_focused_learning: str


class CareerMonthlySteps(BaseModel):
    """Monthly strategic career goals."""

    visionary_planning: str
    high_impact_project: str
    industry_engagement: str
    mentorship: str


class CareerRoutine(BaseModel):
    """Full set of career routines."""

    daily_steps: CareerRoutineSteps
    weekly_steps: CareerWeeklySteps
    monthly_steps: CareerMonthlySteps


# ==== Finance Routine Models ====
class FinanceRoutineSteps(BaseModel):
    """Daily personal finance practices."""

    financial_review: str
    investment_research: str
    wealth_mindset_practice: str


class FinanceWeeklySteps(BaseModel):
    """Weekly finance planning and learning."""

    portfolio_review: str
    smart_spending: str
    growth_oriented_networking: str
    financial_education: str


class FinanceMonthlySteps(BaseModel):
    """Monthly investment and vision planning."""

    investment_strategy_update: str
    set_financial_milestones: str
    philanthropy_focus: str
    long_term_financial_vision: str


class FinanceRoutine(BaseModel):
    """Full set of finance routines."""

    daily_steps: FinanceRoutineSteps
    weekly_steps: FinanceWeeklySteps
    monthly_steps: FinanceMonthlySteps


# ==== Relationship Routine Models ====
class RelationshipRoutineSteps(BaseModel):
    """Daily connection and reflection activities."""

    connection_time: str
    self_reflection_on_relationships: str
    communication_practice: str


class RelationshipWeeklySteps(BaseModel):
    """Weekly bonding and relationship development."""

    intentional_date_quality_time: str
    social_connections: str
    personal_growth_together: str
    team_bonding: str


class RelationshipMonthlySteps(BaseModel):
    """Monthly relationship milestones and retreats."""

    mentorship_support: str
    family_partner_retreats: str
    reflect_on_boundaries: str
    celebrate_milestones: str


class RelationshipRoutine(BaseModel):
    """Full set of relationship routines."""

    daily_steps: RelationshipRoutineSteps
    weekly_steps: RelationshipWeeklySteps
    monthly_steps: RelationshipMonthlySteps


# ==== Daily Routine Block ====
class DailyRoutine(BaseModel):
    """Routine structure for morning, workday, and evening."""

    morning_routine: Dict[str, str]
    workday_routine: Dict[str, str]
    evening_routine: Dict[str, str]


# ==== Final Combined Routine Model ====
class FullRoutine(BaseModel):
    """Top-level model combining all life domains."""

    career: CareerRoutine
    finance: FinanceRoutine
    relationships: RelationshipRoutine
    daily_routine: DailyRoutine


# ------------------------------
# Routine Generator
# ------------------------------
class RoutineGenerator(BaseGenerator):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RoutineGenerator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def _validate(
        payload: Dict[str, Any],
        payload_type: str = PAYLOAD_CATEGORY.ROUTINE_GENERATOR_DATA,
    ) -> None:
        return ValidationManager(validation_type=payload_type).validate(payload)

    def generate(self, payload: Dict[str, Any]) -> Any:
        # load the output-schema for system prompt from JSON file
        parent_path = os.path.dirname(__file__).split("/")[:-2]
        relative_schema_path = ["schema", "routine_schema.json"]
        parent_path.extend(relative_schema_path)
        schema_path = "/".join(parent_path)

        with open(schema_path, "r", encoding="utf-8") as f:
            output_schema = json.load(f)

        # build system prompt with the JSON schema under OUTPUT_FORMAT
        system_prompt = prompt_factory.build_prompt(
            prompt_type=PROMPT_TYPE.SYSTEM_PROMPT,
            prompt_category=PROMPT_CATEGORY.ROUTINE_GENERATOR,
            schema={"OUTPUT_FORMAT": output_schema},
        )

        # build user prompt with actual user data under USER_DATA
        user_prompt = prompt_factory.build_prompt(
            prompt_type=PROMPT_TYPE.USER_PROMPT,
            prompt_category=PROMPT_CATEGORY.ROUTINE_GENERATOR,
            schema={"USER_DATA": payload},
        )

        raw_output = GroqAIClient.get_response(
            system_prompt=system_prompt, user_prompt=user_prompt
        )

        # parse the output using the PydanticOutputParser
        output_parser = PydanticOutputParser(pydantic_object=FullRoutine)
        parsed_result = output_parser.parse(raw_output)
        result = parsed_result.model_dump()
        logger.debug("result: %s", result)

        # validate the parsed result
        self._validate(
            payload=result, payload_type=PAYLOAD_CATEGORY.ROUTINE_GENERATOR_DATA
        )
        return result


# singleton instance of RoutineGenerator
routine_generator = RoutineGenerator()
