from loguru import logger

class AmyController:
    IS_TEXT_INFERING=False
    def __init__(self):
        logger.add("AiAmy.log", level="INFO", rotation="50 MB")
        