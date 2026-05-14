FROM docker.io/python:3.14-slim-trixie AS builder

WORKDIR /install

COPY requirements.txt .

RUN python -m venv /venv && \
    . /venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM docker.io/python:3.14-slim-trixie AS final

ENV PATH="/venv/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m appuser && chown appuser:appuser /app

COPY --from=builder /venv /venv

COPY --chown=appuser:appuser . /app

USER appuser

EXPOSE 8000

ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0"]
CMD [ "--port", "8000"]