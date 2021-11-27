#!/bin/bash

set -e

sleep 15  # wait for debezium/postgresql/redis to start properly

echo "Creating tables in the database"
python models.py

echo "Starting scheduled statement gymnastics"
while true; do
  sleep 5
  python app.py
done
