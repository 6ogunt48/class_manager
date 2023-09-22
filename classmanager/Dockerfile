# pull official base image
FROM python:3.11.5-slim-bullseye

# create directory for the app user
RUN mkdir -p /home/production/web

# create the app user
RUN addgroup --system app && adduser --system --group app
ENV HOME=/home/production APP_HOME=/home/production/web
WORKDIR $APP_HOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ENVIRONMENT=prod TESTING=0

# install system dependencies
RUN apt-get update && apt-get -y install netcat gcc postgresql curl && apt-get clean

# install python dependencies
RUN pip install --upgrade pip && pip install poetry
COPY poetry.lock pyproject.toml $APP_HOME
RUN poetry config virtualenvs.create false && poetry install --no-interaction

# add app
COPY ./application $APP_HOME

# chown all the fules to the app user
RUN chown -R app:app $HOME

# change to the app user
USER app

# run gunicorn
CMD gunicorn --bind 0.0.0.0:$PORT web.application.main:app -k uvicorn.workers.UvicornWorker
