from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger

from api.core.cache import RedisCache, get_redis
from api.core.config import settings
from api.core.database import AsyncDatabase, get_db
from api.core.limiter import limiter

api_router = APIRouter(prefix="/v1/health")


@api_router.get(
    path="",
    status_code=200,
    name="health_check",
    summary="Health Check",
    description="Endpoint para verificar a saúde da API.",
    response_description="A API está saudável.",
)
@limiter.exempt
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}


@api_router.get(
    path="/live",
    status_code=200,
    name="liveness_check",
    summary="Liveness Check",
    description="Endpoint para verificar se a API está viva.",
    response_description="A API está viva.",
)
@limiter.exempt
async def liveness_check():
    return {"status": "alive"}


@api_router.get(
    path="/ready",
    status_code=200,
    name="readiness_check",
    summary="Readiness Check",
    description="Endpoint para verificar se a API está pronta para receber requisições.",
    response_description="A API está pronta para receber requisições.",
)
@limiter.exempt
async def readiness_check(
    mongodb: AsyncDatabase = Depends(get_db),  # noqa: B008
    redis: RedisCache = Depends(get_redis),  # noqa: B008
):
    try:
        await redis.ping()
        await mongodb.command("ping")
        return {"status": "ready", "version": settings.VERSION}
    except Exception:  # noqa: BLE001
        logger.exception("Readiness check failed")

        raise HTTPException(
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            detail="Service is not ready",
        )
