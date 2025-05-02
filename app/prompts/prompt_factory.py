import json
from typing import Any, Dict
from .prompt_map import PROMPT_MAP


class PromptFactory:
    """
    Singleton factory to assemble and retrieve prompts based on type and category.
    """

    _instance: "PromptFactory" = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "PromptFactory":
        if cls._instance is None:
            cls._instance = super(PromptFactory, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @staticmethod
    def assemble_prompt(template: str, schema: Dict[str, Any]) -> str:
        """
        Inject JSON-encoded schema into the template. Any dict or list in schema
        will be JSON-dumped and escaped so braces are preserved.
        """
        safe_schema: Dict[str, Any] = {}
        for key, val in schema.items():
            if isinstance(val, (dict, list)):
                # dump to JSON and escape braces
                js = json.dumps(val)
                safe_schema[key] = js.replace("{", "{{").replace("}", "}}")
            else:
                safe_schema[key] = val

        # python str.format with named placeholders
        return template.format(**safe_schema)

    def build_prompt(
        self, prompt_type: str, prompt_category: str, schema: Dict[str, Any]
    ) -> str:
        """
        Retrieve the system or user prompt template and fill it with provided schema.
        """
        template = PROMPT_MAP[prompt_category][prompt_type]
        return self.assemble_prompt(template, schema)


# singleton instance of PromptFactory
prompt_factory = PromptFactory()
