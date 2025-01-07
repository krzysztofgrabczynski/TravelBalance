FROM python:3.11-alpine

WORKDIR /code

ENV DJANGO_SETTINGS_MODULE core.settings
ENV PYTHONUNBUFFERED 1
ENV PATH "/root/.local/bin:$PATH"

RUN apk add --no-cache curl \
    && curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.5 python3 - \
    && apk add --no-cache postgresql-dev musl-dev

COPY poetry.lock pyproject.toml /code/

COPY . /code/

RUN poetry config virtualenvs.create false && poetry install
