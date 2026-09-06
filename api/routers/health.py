from fastapi import APIRouter

from api.core.config import settings
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
