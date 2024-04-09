from el8.ext.fastapi.auth import unauthenticated
from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.models.error_response import ErrorResponse
from app.services.health_service import HealthException, HealthService

router = APIRouter()


@unauthenticated(router)
@router.get(
    "/health/ready",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"model": ErrorResponse}},
)
async def get_ready(health_service: HealthService = Depends()) -> Response:
    try:
        health_service.get_ready()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HealthException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=e.detail
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="An unexpected error has occurred",
        ) from e


@unauthenticated(router)
@router.get("/health/live", status_code=status.HTTP_204_NO_CONTENT)
async def get_live(health_service: HealthService = Depends()) -> Response:
    health_service.get_live()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
