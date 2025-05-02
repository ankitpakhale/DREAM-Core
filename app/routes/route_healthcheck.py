from app.framework import App
from app.utils import logger, handle_response
from app.utils.constants import ROUTES


class HealthcheckRoute:
    """
    Singleton class to handle and register routes for healthcheck.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    @handle_response
    def _healthcheck_handler():
        """
        Handle the healthcheck of the system.
        """
        logger.debug("_healthcheck_handler route called")
        return {
            "payload": {},
            "message": "PONG",
            "status_code": 200,
        }

    def register(self):
        """
        Register the route for healthcheck.
        """
        App.add_api_route(
            path=ROUTES.HEALTHCHECK_ROUTE,
            endpoint=self._healthcheck_handler,
            methods=["GET"],
        )


# Singleton instance of HealthcheckRoute
healthcheck_route_obj = HealthcheckRoute()
