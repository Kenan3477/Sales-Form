#!/bin/bash
# Railway startup script for ASIS Research Platform

# Set default PORT if not provided by Railway
export PORT=${PORT:-8000}

echo "Starting ASIS Research Platform on port $PORT"
echo "Environment: $ENVIRONMENT"
echo "Database URL configured: $([ ! -z "$DATABASE_URL" ] && echo "Yes" || echo "No")"
echo "Redis URL configured: $([ ! -z "$REDIS_URL" ] && echo "Yes" || echo "No")"

# Start the application
exec gunicorn --bind 0.0.0.0:$PORT --workers 4 --worker-class uvicorn.workers.UvicornWorker main:app
