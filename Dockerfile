# Build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Install dependencies
RUN pip install --no-cache /wheels/*

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create directory for SQLite database
RUN mkdir -p /app/data && \
    chmod 777 /app/data

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=customer_order_service.settings
ENV DATABASE_URL=sqlite:///app/data/db.sqlite3

EXPOSE 8000

CMD ["gunicorn", "customer_order_service.wsgi:application", "--bind", "0.0.0.0:8000"]