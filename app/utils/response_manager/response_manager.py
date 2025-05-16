# app/utils/response_manager.py

from typing import Callable, Any, Dict
from functools import wraps
import inspect

from app.framework import Response, JSONResponse
from app.utils import logger
from json.decoder import JSONDecodeError
from jsonschema.exceptions import ValidationError


class ResponseManager:
    """
    Class to handle standardized response and exception handling logic.
    """

    EXCEPTION_MAPPING = {
        JSONDecodeError: {
            "status_code": 502,
            "message": lambda e: f"Dream JSON Decode Error: {e}",
        },
        ValidationError: {
            "status_code": 400,
            "message": lambda e: f"Dream Validation Error: {e.message}",
        },
        AssertionError: {
            "status_code": 400,
            "message": lambda e: f"Dream Assertion Error: {e}",
        },
        ValueError: {
            "status_code": 400,
            "message": lambda e: f"Dream Invalid value provided: {e}",
        },
        KeyError: {
            "status_code": 400,
            "message": lambda e: f"Dream Missing required key: {e}",
        },
        FileNotFoundError: {
            "status_code": 404,
            "message": lambda e: f"Dream File Not Found: {e}",
        },
        PermissionError: {
            "status_code": 403,
            "message": lambda e: f"Dream Permission Denied: {e}",
        },
        EnvironmentError: {
            "status_code": 401,
            "message": lambda e: f"Dream Environment Error: {e}",
        },
        Exception: {
            "status_code": 500,
            "message": lambda e: f"Dream Internal Server Error: {e}",
        },
    }

    def __init__(self) -> None:
        self.status_code = 200

    def set_status(self, status_code: int) -> None:
        self.status_code = status_code
        Response.status = status_code

    def handle_exception(self, exception: Exception) -> Dict[str, Any]:
        exc_type = type(exception)
        info = self.EXCEPTION_MAPPING.get(exc_type, self.EXCEPTION_MAPPING[Exception])
        msg = (
            info["message"](exception) if callable(info["message"]) else info["message"]
        )
        logger.critical(f"Error ({info['status_code']}): {msg}", exc_info=True)

        self.set_status(info["status_code"])

        return JSONResponse(
            status_code=info["status_code"],
            content={
                "status": False,
                "payload": {},
                "message": msg,
                "status_code": info["status_code"],
            },
        )

    def handle_success(self, result: Dict[str, Any]) -> JSONResponse:
        status_code = result.get("status_code", 200)
        self.set_status(status_code)
        return JSONResponse(
            status_code=status_code,
            content={
                "status": True,
                "payload": result.get("payload", {}),
                "message": result.get("message", "Success"),
                "status_code": status_code,
            },
        )


def handle_response(func: Callable) -> Callable:
    """
    Decorator to wrap a function with centralized response handling.
    """
    manager = ResponseManager()

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Dict[str, Any]:
        try:
            # call original; if it returns a coroutine, await it
            result = func(*args, **kwargs)
            if inspect.isawaitable(result):
                result = await result
            return manager.handle_success(result)
        except tuple(ResponseManager.EXCEPTION_MAPPING.keys()) as e:
            return manager.handle_exception(e)

    return wrapper
