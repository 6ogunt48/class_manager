###########
# BUILDER #
###########

# pull official base image
FROM python:3.11.5-slim-bullseye as builder


# install system dependencies
RUN apt-get update && apt-get -y install netcat gcc postgresql curl && apt-get clean

# set work directory
WORKDIR /wheels

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

# install dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir poetry

COPY poetry.lock pyproject.toml ./


# Generate wheels
RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction && poetry build -n -f wheel && \
    pip wheel . --wheel-dir /wheels

#########
# FINAL #
#########

# Pull official base image
FROM python:3.11.5-slim-bullseye

# Create directory for the app user
ENV HOME=/home/app APP_HOME=/home/app/web PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR $APP_HOME

# Install dependencies
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl && rm -rf /wheels

# Copy application files and set permissions
COPY ./application $APP_HOME
RUN addgroup --system app && adduser --system --group app && chown -R app:app $HOME

# Switch to non-root user
USER app

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "web.application.main:app", "-k", "uvicorn.workers.UvicornWorker"]
