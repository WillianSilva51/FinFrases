from fastapi import APIRouter

from api.core.config import settings
from api.routers.health import api_router as health_router
from api.routers.quotes import api_router as quotes_router

main_router = APIRouter(prefix=settings.API_PREFIX)

main_router.include_router(quotes_router, tags=["Frases"])
main_router.include_router(health_router, tags=["Health"])
