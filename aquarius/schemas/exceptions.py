from loguru import logger


class CustomError(Exception):
    """
    Custom error base class for common errors such as Bad Request,
    Not Found and Unprocessable Entity.
    Can be used to create your own custom error but as a last resort.
    Will be caught by middleware to raise the relavant HTTP Status Code.
    """

    def __init__(self, user_message: str, internal_logging_message: str = "") -> None:
        super().__init__(user_message)
        self.user_message = user_message
        logger.error(internal_logging_message or user_message)
