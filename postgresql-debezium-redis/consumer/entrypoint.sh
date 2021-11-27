#!/bin/bash

set -e

sleep 5  # wait for redis to start properly

echo "Listening to Redis Streams"
python app.py
