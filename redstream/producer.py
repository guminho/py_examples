from contextlib import asynccontextmanager

import redis_client
from fastapi import FastAPI

# Stream configuration
STREAM_NAME = "mystream"
MAX_CAPACITY = 10


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_client.init()
    yield
    await redis_client.close()


app = FastAPI(title="Redis Stream Producer", lifespan=lifespan)


@app.post("/send")
async def send_message(message: str):
    """
    Add a message to the Redis stream with maximum capacity.
    """
    r = redis_client.get()

    # XADD with approximate trimming (~) for better performance
    # Using '*' to auto-generate the ID
    entry_id = await r.xadd(
        STREAM_NAME,
        {"content": message},
        maxlen=MAX_CAPACITY,
        approximate=True,
    )
    return {"status": "sent", "id": entry_id, "message": message}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
