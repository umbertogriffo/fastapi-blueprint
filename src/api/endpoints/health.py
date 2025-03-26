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
    return {"status": "OK"}
