FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get clean && apt-get update -y \
    && apt-get install --no-install-recommends -y \
    python3-dev

COPY requirements.txt /tmp/
RUN pip install --upgrade pip --no-cache-dir -r /tmp/requirements.txt

RUN mkdir -p /src
COPY src/ /src/
COPY tests/ /tests/
