FROM python:3.12.7-slim AS builder

COPY poetry.lock pyproject.toml ./

RUN python -m pip install poetry>=1.8.2 && \
    poetry export -o requirements.prod.txt --without-hashes && \
    poetry export --with=dev -o requirements.dev.txt --without-hashes

FROM python:3.12.7-slim AS dev

WORKDIR /app
COPY --from=builder requirements.dev.txt /app

RUN apt update -y && apt install --no-install-recommends -y \
    python3-dev && \
    pip install --upgrade pip --no-cache-dir --user -r requirements.dev.txt && \
    apt clean && rm -rf /var/lib/apt/lists/* requirements.dev.txt

FROM python:3.12.7-slim AS runtime-image

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PATH=/root/.local/bin:$PATH

COPY --from=dev /root/.local /root/.local
COPY src/ /app/src
COPY tests/ /app/tests
COPY alembic.ini /app/alembic.ini
