from typing import Union
from app.services.validation_manager.strategy import (
    user_form_data,
    routine_generator_data,
    daily_habit_generator_data,
    fear_and_motivation_generator_data,
)
from app.utils import logger
from app.utils.constants import PAYLOAD_CATEGORY

STRATEGY_MAP = {
    PAYLOAD_CATEGORY.USER_FORM_DATA: user_form_data,
    PAYLOAD_CATEGORY.ROUTINE_GENERATOR_DATA: routine_generator_data,
    PAYLOAD_CATEGORY.FEAR_AND_MOTIVATION_GENERATOR_DATA: fear_and_motivation_generator_data,
    PAYLOAD_CATEGORY.DAILY_HABIT_GENERATOR_DATA: daily_habit_generator_data,
}


class ValidationManager:
    def __init__(self, validation_type: str) -> None:
        self.strategy = STRATEGY_MAP[
            validation_type
        ]  # if validation_type is not in STRATEGY_MAP then it will automatically throw error
        logger.debug(f"{validation_type} strategy assigned for validation")

    def validate(self, payload: Union[list, dict]) -> bool:
        return self.strategy.validate(payload=payload)
