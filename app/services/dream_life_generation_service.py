from typing import Dict, Any
from app.utils import retry
from app.services.validation_manager import ValidationManager
from app.utils import id_generator
from app.config import GeneralConfig
from app.utils.constants import PAYLOAD_CATEGORY
from .generators import (
    routine_generator,
    fear_and_motivation_generator,
    daily_habit_generator,
)


class DreamLifeGenerationService:
    """
    A service for Dream Life Generation with request/response validation and GroqAIClient-based generation.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DreamLifeGenerationService, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    @staticmethod
    @retry(max_retries=GeneralConfig.RETRY_COUNT, delay=1, backoff=2)
    def execute_task(payload: Dict[str, str]) -> Any:
        """
        Executes a task by validating the request,
        interacting with the GroqAIClient to generate a Dream Life,
        and then validating and assigning IDs to the response.
        """

        # validate request payload
        ValidationManager(validation_type=PAYLOAD_CATEGORY.USER_FORM_DATA).validate(
            payload
        )

        # TODO: Rename *_generator to some other meaningful name, generator name belongs to py generator
        dream_life = {
            "routine": routine_generator.generate(payload),
            "fear_and_motivation": fear_and_motivation_generator.generate(payload),
            "daily_habit": daily_habit_generator.generate(payload),
        }

        # add IDs & return it
        initial_dream_life_result_with_ids = id_generator.assign_ids(dream_life)
        return initial_dream_life_result_with_ids


# singleton instance of DreamLifeGenerationService
dream_life_generation_service = DreamLifeGenerationService()
