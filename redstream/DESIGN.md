# Design Rationale: Redis Stream Demo

This document explains the technical decisions and architecture behind the Redis Stream implementation in this project.

## 1. Producer Design

### FastAPI with Lifespan
We use the FastAPI `lifespan` context manager instead of `startup`/`shutdown` events. This is the modern, recommended way to handle resources like Redis connections, ensuring they are properly initialized before the app starts and closed gracefully when it stops.

### Approximate Trimming (`MAXLEN ~ 50`)
When adding messages with `XADD`, we use the `~` (approximately) operator with `MAXLEN`.
- **The Problem**: Exact trimming is an $O(N)$ operation where $N$ is the number of evicted items.
- **The Solution**: Approximate trimming only removes items when a whole internal macro-node can be freed. This makes the operation nearly $O(1)$, which is critical for high-throughput producers.

---

## 2. Consumer Design

### Consumer Groups
The system uses Redis Consumer Groups (`XGROUP`) to distribute work among multiple workers. This ensures that:
1. Each message is processed by only one worker in the group.
2. We can scale horizontally by adding more workers.

### Reliability and the PEL (Pending Entries List)
To ensure **zero message loss** while minimizing log noise and redundant calls, the consumer implements a stateful two-step reading strategy:

#### Step 1: Recover from Crashes (ID `0`)
On startup, the worker enters a "Pending Recovery" state. It reads from the stream using ID `0`, which tells Redis: *"Give me messages that were delivered to ME but I never acknowledged."*

The worker remains in this state until the Pending Entries List (PEL) for this specific consumer is completely empty. This ensures that if a worker crashes mid-processing, it finishes its leftover work before taking on new tasks.

#### Step 2: New Work (ID `>`)
Once the pending list is exhausted, the worker switches to a "Listening" state using ID `>`. This tells Redis: *"Give me messages that have never been delivered to any consumer in this group."*

In this state, the worker uses `BLOCK` to wait efficiently for new data. It only reverts to "Step 1" if a system error occurs or during a restart, significantly reducing log noise and unnecessary polling.

### Acknowledgment (`XACK`)
Messages are only acknowledged *after* the simulated work (`asyncio.sleep(5)`) is complete. If the worker fails during sleep, the message remains in the PEL and will be picked up again during the "Step 1" recovery phase.

---

## 3. Concurrency and Scaling

### Unique Consumer Names
Every worker instance must have a unique name within the group. The implementation allows passing a name via CLI or defaults to a PID-based name. This uniqueness is what allows Redis to track individual Pending Entries Lists correctly.

### Blocking Reads (`BLOCK`)
The consumer uses the `BLOCK` parameter in `XREADGROUP`. This is a "push" model where the worker waits for data rather than polling the server, reducing CPU usage and latency.
