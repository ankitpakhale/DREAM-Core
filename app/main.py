from app.framework import uvicorn
from app.config.general_config import GeneralConfig
from app.utils import logger
from app.routes.route_manager import RouteManager

# TODO: Think about changing name of Routes layer to Presentation layer
# instantiate and load routes dynamically
route_manager = RouteManager()
logger.debug("Loading all Routes...")
route_manager.load_routes()
logger.debug("Registering all Routes...")
route_manager.register_all()
logger.debug("All Routes are Registered")

if __name__ == "__main__":
    __port = GeneralConfig.APP_PORT
    __host = GeneralConfig.APP_HOST
    logger.debug(f"➡ Starting server on port {__port} and host {__host}...")
    uvicorn.run(
        "app.framework:App",
        host=__host,
        port=__port,
        reload=False if GeneralConfig.ENV.lower() == "prod" else True,
    )
