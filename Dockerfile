FROM python:3.12.5-slim-bookworm AS builder

COPY poetry.lock pyproject.toml ./

RUN python -m pip install poetry>=1.8.2 && \
    poetry export -o requirements.prod.txt --without-hashes && \
    poetry export --with=dev -o requirements.dev.txt --without-hashes

FROM python:3.12.5-slim-bookworm AS dev

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder requirements.dev.txt /app

RUN apt clean && apt update -y && apt install --no-install-recommends -y \
    python3-dev && \
    pip install --upgrade pip --no-cache-dir -r \
    requirements.dev.txt && \
    rm requirements.dev.txt

COPY src/ /app/src
COPY tests/ /app/tests
