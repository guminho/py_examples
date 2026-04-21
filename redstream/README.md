# Redis Stream Demo

A robust implementation of Redis Streams using Python, FastAPI, and Asyncio.

For a detailed explanation of the architecture, reliability patterns, and performance optimizations, see [DESIGN.md](DESIGN.md).

## Quick Start

### 1. Setup
Ensure you have Redis running on `localhost:6379`.

```bash
uv sync
```

### 2. Start the Producer
The producer provides an HTTP endpoint to add messages to the stream.

```bash
uv run uvicorn producer:app --reload --port 8000
```

### 3. Start Consumers
You can run multiple consumers to distribute the load. Each should have a unique name.

```bash
# Terminal 1
uv run python consumer.py worker-1

# Terminal 2
uv run python consumer.py worker-2
```

### 4. Send Messages
```bash
curl -X POST "http://localhost:8000/send?message=HelloRedis"
```

## Testing Reliability
1. Send a message.
2. Kill a worker while it's "processing" (during the 5s sleep).
3. Restart the worker with the **same name**.
4. Observe it picking up the **pending message** before processing any new ones.
