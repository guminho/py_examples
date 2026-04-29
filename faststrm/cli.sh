#!/usr/bin/env bash

curl -s -X POST http://localhost:8000/send \
  -H "Content-Type: application/json" \
  -d '{"user_name": "mera", "user_id": 15}'
