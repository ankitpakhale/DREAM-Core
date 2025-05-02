from typing import Dict, Any
from uuid import uuid4


class IDGenerator:
    """
    Utility class for generating and assigning unique IDs.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(IDGenerator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def assign_ids(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Iterates over payload to assign a uuid4
        """
        return {
            **payload,
            "id": (str(uuid4())),
        }


# singleton instance of IDGenerator
id_generator = IDGenerator()
