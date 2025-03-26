import time

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from utils.log import get_logger

logger = get_logger()


class LogMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware to log the incoming requests and their corresponding responses.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Logs the incoming request and its response.

        Args:
            request (Request): The incoming request.
            call_next: The next middleware in the chain.

        Returns:
            Response: The response from the next middleware in the chain.
        """
        logger.info(
            "Request",
            extra={
                "request": {
                    "method": request.method,
                    "url": str(request.url),
                },
            },
        )

        start_time = time.time()
        response: Response = await call_next(request)
        process_time = time.time() - start_time

        logger.info(
            "Response",
            extra={
                "request": {
                    "method": request.method,
                    "url": str(request.url),
                },
                "response": {"status_code": response.status_code},
                "process_time": process_time,
            },
        )
        return response
