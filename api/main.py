from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from api.core.database import init_db
from api.core.exceptions.custom_exceptions import (
    DomainValidationException,
    ResourceNotFoundException,
)
from api.core.handlers.exception_handlers import (
    domain_validation_handler,
    global_exception_handler,
    http_handler,
    request_validation_handler,
    resource_not_found_handler,
)
from api.core.limiter import limiter
from api.routers.health import api_router as health_router
from api.routers.quotes import api_router as quotes_router

tags_metadata = [
    {
        "name": "Frases",
        "description": "Operações relacionadas a frases financeiras.",
    },
    {
        "name": "Health",
        "description": "Endpoint para verificar a saúde da API.",
    },
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="FinFrases API",
    description="""
API aberta e gratuita para frases de mentalidade financeira 💰

## Funcionalidades:
- Frases sobre investimentos
- Educação financeira
- Mentalidade de riqueza

Totalmente em português (PT-BR).
""",
    summary="Frases de mentalidade financeira em português",
    version="1.0.2",
    openapi_url="/api/openapi.json",
    tags_metadata=tags_metadata,
    contact={
        "name": "Willian Silva",
        "url": "https://github.com/WillianSilva51",
        "email": "antonio.oliveira051@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    docs_url=None,
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

app.state.limiter = limiter


@app.get("/api/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_handler)  # type: ignore
app.add_exception_handler(DomainValidationException, domain_validation_handler)  # type: ignore
app.add_exception_handler(ResourceNotFoundException, resource_not_found_handler)  # type: ignore
app.add_exception_handler(RequestValidationError, request_validation_handler)  # type: ignore
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(quotes_router, prefix="/api", tags=["Frases"])
app.include_router(health_router, prefix="/api", tags=["Health"])
