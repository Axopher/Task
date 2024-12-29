#!/bin/bash

# Wait for the PostgreSQL database to be ready
echo "Waiting for database to be ready..."

# Loop until the database is accessible
until nc -z -v -w30 db 5432; do
  echo "Waiting for PostgreSQL database to start..."
  # Wait for 15 seconds before checking again
  sleep 15
done

# Once the database is available, run Django migrations
echo "Database is up, running migrations..."
python manage.py migrate

# Finally, run the Django development server
echo "Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000
