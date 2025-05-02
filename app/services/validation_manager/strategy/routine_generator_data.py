from jsonschema import validate
from typing import Dict, Union
from app.services.validation_manager.strategy.base_strategy import BaseStrategy
from app.utils import logger
from app.services.validation_manager.schema_map import SCHEMA_MAP
from app.utils.constants import BOOLEAN_VALUES, PAYLOAD_CATEGORY


class RoutineGeneratorData(BaseStrategy):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RoutineGeneratorData, cls).__new__(
                cls, *args, **kwargs
            )
        return cls._instance

    @staticmethod
    def _process_payload(payload: Dict[str, str]) -> Dict[str, bool]:
        for key, value in payload.items():
            # check if the value is a string,
            # and the value is either "true" or "false" (case-insensitive)
            if isinstance(value, str) and value.lower() in {
                BOOLEAN_VALUES.TRUE,
                BOOLEAN_VALUES.FALSE,
            }:
                # convert "true" to True and "false" to False by comparing lowercase value
                payload[key] = value.lower() == BOOLEAN_VALUES.TRUE

        logger.debug(
            f"{PAYLOAD_CATEGORY.ROUTINE_GENERATOR_DATA.replace("_", " ").title()} processed successfully!!!"
        )
        return payload

    def _validate(self, payload: Dict[str, str], schema: Dict) -> None:
        __payload = self._process_payload(payload)
        validate(instance=__payload, schema=schema)
        logger.debug(
            f"{PAYLOAD_CATEGORY.ROUTINE_GENERATOR_DATA.replace("_", " ").title()} validated successfully!!!"
        )

    def validate(self, payload: Union[list, dict]) -> None:
        schema = SCHEMA_MAP[PAYLOAD_CATEGORY.ROUTINE_GENERATOR_DATA]
        return self._validate(payload=payload, schema=schema)


# singleton instance of RoutineGeneratorData
routine_generator_data = RoutineGeneratorData()
