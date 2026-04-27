FROM python:3.14

ENV UV_SYSTEM_PYTHON=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get clean && apt-get update && apt-get install -y locales \
    && sed -i '/es_ES.UTF-8/s/^# //' /etc/locale.gen \
    && locale-gen

COPY pyproject.toml uv.lock /app/
RUN cd /app && uv sync --frozen --no-install-project

RUN mkdir -p /app/manolibakes /app/data

COPY manolibakes /app/manolibakes

WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["python3", "/app/manolibakes/manage.py", "runserver", "0.0.0.0:8000"]