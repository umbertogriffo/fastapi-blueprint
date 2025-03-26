import json

from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette import status
from utils.log import get_logger

logger = get_logger()


async def validation_exception_handler(request: Request, exc):
    """
    The exception handler to intercept RequestValidationError and ValidationError making sure we’ll have a consistent
    error response format.
    The first argument is the request object, and the second argument is the exception object.

    Args:
        request: The request that caused the exception.
        exc: The exception object that was raised.
    Returns:
        A JSON response with the error code and message.
    """
    exc_json = jsonable_encoder({"detail": exc.errors(), "body": exc.body})

    response = {"detail": []}
    for error in exc_json["detail"]:
        response["detail"].append(f"{error['loc'][-1]}: {error['msg']}")

    logger.error(
        f"The client sent invalid data!: {json.dumps(response)}",
        exc_info=True,
        stack_info=True,
    )

    return JSONResponse(response, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
