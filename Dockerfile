# --- Base Stage: Shared dependencies ---
FROM python:3.13-slim AS base

RUN apt-get update && apt-get install -y \
    pkg-config default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# --- Development Stage: Runs as root ---
FROM base AS development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# --- Production Stage: Runs as 'app' user ---
FROM base AS production
RUN addgroup --system app && adduser --system --group app && \
    chown -R app:app /app

USER app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
