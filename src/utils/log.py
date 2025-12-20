import datetime
import json
import logging
import sys
from logging import Formatter
from logging.handlers import RotatingFileHandler

from config import settings


def convert_timestamp_to_date(timestamp: float) -> str:
    """
    Converts a Unix timestamp to a formatted date-time string.

    Args:
        timestamp (float): The Unix timestamp to be converted.

    Returns:
        str: The formatted date-time string in the format 'YYYY-MM-DD HH:MM:SS,mmm'.
    """
    # Convert the timestamp to a datetime object
    dt_object = datetime.datetime.fromtimestamp(timestamp)

    # Format the datetime object to the desired string format
    formatted_time = dt_object.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]

    return formatted_time


class JsonFormatter(Formatter):
    """
    Subclassing `logging.Formatter` and overriding the format method.
    This method takes in the log record, using which we can construct our JSON log record.
    We then add our formatter to the Root logger, remove other handlers and import this new logger module into our
    main application.
    """

    def __init__(self):
        super(JsonFormatter, self).__init__()

    def _log_record_to_dict(self, record: logging.LogRecord) -> dict:
        json_record = {
            "timestamp": convert_timestamp_to_date(record.created),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        request = record.__dict__.get("request")
        response = record.__dict__.get("response")
        process_time = record.__dict__.get("process_time")

        if request:
            json_record["request"] = request
        if response:
            json_record["response"] = response
        if process_time:
            json_record["process_time"] = process_time
        if record.levelno == logging.ERROR and record.exc_info:
            json_record["error"] = self.formatException(record.exc_info)
        if record.levelno == logging.ERROR and record.stack_info:
            json_record["trace"] = record.stack_info

        return json_record

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the log record into a JSON string.

        Args:
            record: The log record to be formatted.

        Returns:
            A JSON string representation of the log record.
        """
        return json.dumps(self._log_record_to_dict(record))


def get_logger():
    logger = logging.root
    logger.setLevel(settings.LOG_LEVEL)

    # Prevent double configuration by checking handlers
    if not logger.hasHandlers():
        # Disable the uvicorn.access logger since we are logging using the `LogMiddleware` middleware
        logging.getLogger("uvicorn.access").disabled = True
        logging.getLogger("uvicorn.access").propagate = False

        # Set SQLAlchemy engine logger level
        # https://docs.sqlalchemy.org/en/20/core/engines.html#configuring-logging
        logging.getLogger("sqlalchemy.engine").setLevel(settings.LOG_LEVEL)
        logging.getLogger("sqlalchemy.engine").propagate = settings.LOG_DATABASE_QUERIES
        logging.getLogger("sqlalchemy.pool").setLevel(settings.LOG_LEVEL)

        # Stream handler to stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(settings.LOG_LEVEL)
        handler.setFormatter(
            JsonFormatter()
        )  # Set a JSON formatter for structured logging
        logger.addHandler(handler)

        # File handler (if needed)
        if settings.LOG_SAVE_ON_FILE:
            # Define a handler that writes log messages to a file with rotation
            file_handler = RotatingFileHandler(
                filename="app.log",
                maxBytes=10 * 1024 * 1024,
                backupCount=5,  # 10 MB per file, keep 5 files
            )
            file_handler.setFormatter(JsonFormatter())
            logger.addHandler(file_handler)

    return logger
