import logging
from logging import Logger

def configure_logging(level: int = logging.INFO) -> Logger:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    logger = logging.getLogger("jpn_weather_bot")
    logger.setLevel(level)
    return logger
