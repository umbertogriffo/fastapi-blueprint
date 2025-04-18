import uuid
from dataclasses import dataclass

from starlette import status
from utils.log import get_logger

logger = get_logger()

"""
Exceptions used in the Backend Service.
"""


@dataclass
class ErrorContent:
    message: str
    http_status_code: int


class BackendException(Exception):
    """Base class for all Backend Service errors."""

    default_message: str = "An Unexpected error occurred"
    http_status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class ValueRequired(BackendException):
    """
    Raised when a required value is not provided.
    """

    default_message = "A required value is not provided"
    http_status_code: int = status.HTTP_400_BAD_REQUEST


class InvalidValue(BackendException):
    """
    Raised when a value doesn’t meet some criteria.
    """

    default_message = "A value doesn't meet the required criteria"
    http_status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY


# Dictionary of errors that we want to propagate and expose to the API users
ERRORS = {
    ValueRequired: ErrorContent(
        ValueRequired.default_message, ValueRequired.http_status_code
    ),
    InvalidValue: ErrorContent(
        InvalidValue.default_message, InvalidValue.http_status_code
    ),
}


def get_error_content(exception: Exception) -> ErrorContent:
    """
    This function takes an exception object as input and returns an instance of ErrorContent.

    It uses a dictionary lookup to retrieve an error message associated with the type of exception,
    or creates a default error message if the exception type is not found in the ERRORS mapping.

    The function then generates a unique ID for the error, combines it with the error message and
    exception details, and returns an ErrorContent object containing this information along with
    the appropriate HTTP status code.

    Args:
        exception (Exception): An instance of Exception that was raised during execution.

    Returns:
        ErrorContent: An instance of ErrorContent containing the error message, unique ID,
                      exception details, and associated HTTP status code.
    """
    error = ERRORS.get(
        type(exception),
        ErrorContent(
            "Unexpected error while processing the request",
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        ),
    )
    error_message = f"{str(uuid.uuid4())} | {error.message}: {str(exception)}"
    http_status_code = error.http_status_code

    return ErrorContent(error_message, http_status_code)
