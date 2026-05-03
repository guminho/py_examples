# faststrm

FastAPI + FastStream example using Redis Streams.

## Prerequisites

- Python 3.13+
- Redis running on `localhost:6379`

## Install

```bash
uv sync
```

## Run

Start the worker and server in separate terminals:

```bash
# Terminal 1 — worker (consumes from Redis streams)
faststream run worker_app:app

# Terminal 2 — server (FastAPI HTTP publisher)
uvicorn server_app:app
```

## Usage

```bash
curl -s -X POST http://localhost:8000/send \
  -H "Content-Type: application/json" \
  -d '{"user_name": "mera", "user_id": 15}'
```

## AsyncAPI Docs

```bash
faststream docs gen worker_app:app
faststream docs serve asyncapi.json
```
