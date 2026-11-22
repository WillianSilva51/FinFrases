from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi import get_scalar_api_reference
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from api.core.config import settings
from api.core.database import close_db, init_db
from api.core.exceptions.custom_exceptions import (
    DomainValidationException,
    ResourceAlreadyExistsException,
    ResourceNotFoundException,
)
from api.core.handlers.exception_handlers import (
    domain_validation_handler,
    global_exception_handler,
    http_handler,
    request_validation_handler,
    resource_already_exists_handler,
    resource_not_found_handler,
)
from api.core.limiter import limiter
from api.core.rabbitmq import close_rabbitmq, init_rabbitmq
from api.dependencies.rabbitmq_dependencies import declare_rabbitmq_topology
from api.routers.main_router import main_router

tags_metadata = [
    {
        "name": "Frases",
        "description": "Operações relacionadas a frases financeiras.",
    },
    {
        "name": "Saúde",
        "description": "Endpoint para verificar a saúde da API.",
    },
    {
        "name": "Autenticação",
        "description": "Endpoint para verificar a validade da chave de API.",
    },
    {
        "name": "Assinantes",
        "description": "Operações relacionadas a assinantes.",
    },
]

PREFIX = settings.API_PREFIX


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await init_db()
        await init_rabbitmq()
        await declare_rabbitmq_topology()

        yield

    finally:
        await close_db()
        await close_rabbitmq()


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
    version=settings.VERSION,
    openapi_url=f"{PREFIX}/openapi.json",
    openapi_tags=tags_metadata,
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
    redoc_url=f"{PREFIX}/redoc",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


@app.get(f"{PREFIX}/docs", include_in_schema=False)
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
app.add_exception_handler(
    ResourceAlreadyExistsException,
    resource_already_exists_handler,  # type: ignore
)
app.add_exception_handler(RequestValidationError, request_validation_handler)  # type: ignore
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(main_router)
