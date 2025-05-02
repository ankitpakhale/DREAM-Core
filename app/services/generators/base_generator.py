from typing import Dict, Any
from abc import ABC, abstractmethod


class BaseGenerator(ABC):
    """
    Abstract base service that defines the interface for executing tasks.
    """

    @abstractmethod
    def _validate(type: str, payload: Dict[str, Any]) -> Any:
        """
        Abstract method to validate request & response payload.
        """
        pass

    @abstractmethod
    def generate(self, payload: Dict[str, Any]) -> Any:
        """
        Abstract method that must be implemented to execute a given task using a payload.
        """
        pass
