from . import formatters, handlers
import logging
import logging.config
from app.config import GeneralConfig


logging.config.dictConfig({"disable_existing_loggers": True, "version": 1})


# TODO: name must come from root directory
# TODO: dynamic level
def get_logger(name="DREAM", level="DEBUG"):
    __level = level if GeneralConfig.ENV != "prod" else "CRITICAL"
    logger = logging.getLogger(name=name)

    # remove any existing handlers to avoid duplicates
    for handler in logger.handlers:
        logger.removeHandler(handler)

    # add console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatters.Default())
    logger.addHandler(ch)

    # add custom monthly rotating file handler
    # fh = handlers.monthly_rotating_file_handler()
    # logger.addHandler(fh)

    logger.setLevel(level=__level)
    return logger
