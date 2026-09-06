FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    uv venv && \
    uv sync --frozen --no-install-project

FROM docker.io/library/python:3.13-slim-bookworm AS final

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m appuser && chown appuser:appuser /app

COPY --chown=appuser:appuser . /app

COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv

USER appuser

EXPOSE 8000

ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips=127.0.0.1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"]
