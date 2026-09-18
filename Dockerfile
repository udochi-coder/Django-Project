FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install .

COPY . .

RUN mkdir -p /app/staticfiles /app/mediafiles && \
    python manage.py collectstatic --noinput

EXPOSE 10000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn ResultPortal.wsgi:application --bind 0.0.0.0:${PORT:-10000} --workers 3"]
