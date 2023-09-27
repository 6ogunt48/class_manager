#!/bin/sh
echo "App is waiting for postgres DB ....."

while ! nc -z  app-database 5432; do
  sleep 0.2
done

echo "PostgreSQL started"

exec "$@"