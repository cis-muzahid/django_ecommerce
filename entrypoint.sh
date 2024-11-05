#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Wait for the database to be ready
echo "Waiting for PostgreSQL to be ready..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 1
done
echo "PostgreSQL is ready."

# Run migrations
echo "Running migrations..."
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# Collect static files (optional)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

# Start the server
echo "Starting server..."
exec "$@"
