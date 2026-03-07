FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    pkg-config default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# Install dependencies globally as root
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R app:app /app

USER app
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]