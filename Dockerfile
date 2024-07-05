# Pull base image
FROM python:3.12

ENV POETRY_CACHE_DIR=/tmp/poetry_cache

# Install dependencies
RUN apt-get clean && apt-get update && apt-get install -y locales \
    && sed -i '/es_ES.UTF-8/s/^# //' /etc/locale.gen \
    && locale-gen \
    && pip3 install --upgrade --no-cache-dir pip \
    && pip3 install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/
RUN cd /app \
    && POETRY_VIRTUALENVS_CREATE=false poetry install --no-root\
    && rm -rf $POETRY_CACHE_DIR

RUN mkdir /app/data /app/manolibakes

COPY manolibakes /app/manolibakes

RUN groupadd -r manolibakesgroup \
    && useradd -r -g manolibakesgroup manolibakesuser \
    && chown manolibakesuser:manolibakesgroup -R /app

WORKDIR /app

USER manolibakesuser

EXPOSE 8000

ENTRYPOINT [ "python3", "/app/manolibakes/manage.py", "runserver", "0.0.0.0:8000"]
