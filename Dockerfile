FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn && \
    pip install --no-cache-dir .

COPY . .

RUN mkdir -p /app/staticfiles /app/mediafiles

EXPOSE 8000

CMD ["gunicorn", "ResultPortal.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
