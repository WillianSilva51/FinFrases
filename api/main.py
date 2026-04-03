from contextlib import asynccontextmanager

from api.core.database import init_db
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.routers.quotes import api_router as quotes_router

from api.core.exceptions.custom_exceptions import (
    DomainValidationException,
    ResourceNotFoundException,
)
from api.core.handlers.exception_handlers import (
    http_handler,
    domain_validation_handler,
    resource_not_found_handler,
    request_validation_handler,
    global_exception_handler,
)

tags_metadata = [
    {
        "name": "Frases",
        "description": "Operações relacionadas a frases financeiras.",
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
    version="0.1.0",
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
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)

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
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(quotes_router, prefix="/api")
