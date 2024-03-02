# Pull base image
FROM python:3.10

# Install dependencies
RUN apt-get clean && apt-get update && apt-get install -y locales \
    && sed -i '/es_ES.UTF-8/s/^# //' /etc/locale.gen \
    && locale-gen
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