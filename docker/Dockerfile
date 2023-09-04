FROM python:3.12-slim as base
ARG REQUIREMENTS_PATH=/requirements/requirements.txt
ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1 \
    PYTHONFAULTHANDLER=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

FROM base as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gettext \
    git \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
ARG REQUIREMENTS_PATH=/requirements/requirements.txt
RUN pip wheel --wheel-dir /root/wheels -r "${REQUIREMENTS_PATH}" --no-build-isolation

FROM base

RUN apt-get update && apt-get install -y git

WORKDIR /app
COPY --from=builder /root/wheels /root/wheels
COPY ./requirements /requirements
ARG REQUIREMENTS_PATH=/requirements/requirements.txt
RUN pip install --no-index --find-links=/root/wheels/ -r "${REQUIREMENTS_PATH}" --no-build-isolation

COPY . /app

ENV C_FORCE_ROOT 1
