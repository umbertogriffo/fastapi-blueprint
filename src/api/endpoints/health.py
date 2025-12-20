from database import check_health_safe, engine
from fastapi import APIRouter
from starlette import status

router = APIRouter()


@router.get(
    "/health",
    summary="Perform a simple health check",
    status_code=status.HTTP_200_OK,
    response_description="Return HTTP 200",
)
def health():
    """
    Performs a simple health check.
    """
    return health_check(include_dependencies=False)


@router.get(
    "/health/readiness",
    operation_id="isReady",
    summary="Check if the service and dependencies are healthy; i.e. capable of processing requests.",
    status_code=status.HTTP_200_OK,
    response_description="Return HTTP 200",
)
async def readiness_check():
    return health_check(include_dependencies=True)


@router.get(
    "/health/liveness",  # Explicit requirement
    operation_id="isAlive",
    summary="Check if the service is healthy; i.e. capable of responding to requests.",
    status_code=status.HTTP_200_OK,
    response_description="Return HTTP 200",
)
async def liveness_check():
    return health_check(include_dependencies=False)


def health_check(include_dependencies: bool = False):
    """
    Health check endpoint.

    Args:
        include_dependencies (bool): Whether to include dependency checks.

    Returns:
        dict: Health status.
    """
    # Here you would typically check the health of your dependencies
    # e.g., database connection, external services, etc.
    # For simplicity, we return a static response.

    status_response = {"status": "OK"}

    if include_dependencies:
        # Perform checks for dependencies here
        db_status = check_health_safe(engine)
        status_response["database"] = "OK" if db_status else "FAIL"

    return status_response
