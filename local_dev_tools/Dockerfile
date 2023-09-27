# Pull official base image
FROM python:3.11.5-slim-bullseye

# Set working directory and environment variables
WORKDIR /usr/src/application
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONBUFFERED=1 SECRET_KEY="ddecb1f1cf90ba71f78917b8d59f13e0b0748839204ce235fce82d17b7b0a8ae66c33b76fab41b7fef5735de9de9880660a114b7d9e57f93316de61923c4804b"

# Install system and project dependencies
RUN apt-get update && apt-get -y install netcat gcc postgresql && apt-get clean && pip install --upgrade pip && \
    pip install poetry && poetry config virtualenvs.create false

# Copy requirements and install project dependencies
COPY ./classmanager/pyproject.toml ./classmanager/poetry.lock ./
RUN poetry install

# Copy application code and entrypoint
COPY ./classmanager .
RUN chmod +x ./entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/usr/src/application/entrypoint.sh"]

