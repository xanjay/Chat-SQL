# ------------------- Stage 1: Build Stage ------------------------------
FROM python:3.10-slim AS builder
# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
    curl \
    build-essential \
    libffi-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY . /app

RUN poetry config virtualenvs.create true \
    && poetry install --only main

# ------------------- Stage 2: Final Stage ------------------------------
FROM python:3.10-slim
WORKDIR /app

# Copy from the builder stage
COPY --from=builder /app /app
# Expose port 8501 for the streamlit application
EXPOSE 8501
ENV PATH="/app/.venv/bin:$PATH"

CMD ["streamlit", "run", "src/chat_sql/app.py", "--server.address=0.0.0.0"]