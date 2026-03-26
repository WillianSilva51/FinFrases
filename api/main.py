from fastapi import FastAPI

tags_metadata = [
    {
        "name": "Frases",
        "description": "Operações relacionadas a frases financeiras.",
    },
    {
        "name": "Categorias",
        "description": "Categorias como investimentos, mindset, etc.",
    },
]

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
)
