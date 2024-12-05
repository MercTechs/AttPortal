# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including curl for healthcheck
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry

# Copy poetry files first for better caching
COPY pyproject.toml poetry.lock ./

# Copy the rest of the project
COPY . .

# Configure poetry to not create virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies and the project itself
RUN poetry install --no-interaction --no-ansi

# Install watchfiles for reload support
RUN pip install watchfiles

# Add src directory to PYTHONPATH
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8004

# Command to run the application using poetry script
CMD ["poetry", "run", "start"]