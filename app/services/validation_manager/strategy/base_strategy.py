from abc import ABC, abstractmethod
from typing import Dict


class BaseStrategy(ABC):
    @abstractmethod
    def _process_payload(payload: Dict[str, str]) -> Dict[str, bool]:
        pass

    @abstractmethod
    def _validate(self, payload: Dict[str, str], schema: Dict) -> None:
        pass

    @abstractmethod
    def validate(self, payload: Dict) -> bool:
        pass
