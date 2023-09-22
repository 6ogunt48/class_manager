#!/bin/sh
echo "waiting for postgres..."

while ! nc -z  app-database 5432; do
  sleep 0.2
done

echo "PostgreSQL started"

exec "$@"