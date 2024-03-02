# Pull base image
FROM python:3.10

# ENV LC_ALL="es_ES.UTF-8"
# ENV LC_CTYPE="es_ES.UTF-8"

# Install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY manolibakes /app
COPY data /var/sqlite

RUN groupadd -r manolibakesgroup \
    && useradd -r -g manolibakesgroup manolibakesuser \
    && chown manolibakesuser:manolibakesgroup -R /app \
    && chmod 755 -R /var/sqlite

WORKDIR /app

USER manolibakesuser

ENTRYPOINT [ "python3", "/app/manage.py", "runserver" ]