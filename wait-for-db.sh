#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

echo "Waiting for database at $host..."

until mysqladmin ping -h "$host" -u user1 -pStrongPassword123 --silent; do
  echo "Database is unavailable - sleeping"
  sleep 2
done

echo "Database is up - executing command"
exec $cmd
