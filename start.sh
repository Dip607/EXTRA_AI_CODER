#!/usr/bin/env bash
# start.sh

# Apply database migrations
python manage.py migrate --no-input

# Collect static files
python manage.py collectstatic --no-input

# Start Gunicorn server
gunicorn code_forum.wsgi:application --bind 0.0.0.0:$PORT
