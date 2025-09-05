#!/bin/bash
# ANISA Startup Script

set -e

echo "Starting ANISA Cultural Intelligence Engine..."

# Wait for database to be ready
echo "Waiting for database..."
while ! pg_isready -h ${DB_HOST:-localhost} -p ${DB_PORT:-5432} -U ${DB_USER:-gtcx} 2>/dev/null; do
  echo "Database not ready, waiting..."
  sleep 2
done
echo "Database is ready!"

# Run migrations
echo "Running database migrations..."
alembic upgrade head || echo "Migrations skipped (tables may already exist)"

# Start the application
echo "Starting ANISA API on port ${ANISA_PORT:-8083}..."
exec uvicorn src.api_v2:app \
  --host 0.0.0.0 \
  --port ${ANISA_PORT:-8083} \
  --log-level ${LOG_LEVEL:-info} \
  --access-log
