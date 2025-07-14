import asyncio

from fastapi import FastAPI
from sse_starlette import EventSourceResponse
from sse_starlette import JSONServerSentEvent as SSE

app = FastAPI()


async def gen():
    for i in range(5):
        await asyncio.sleep(0.1)
        yield {"delta": f"content-{i}"}


@app.post("/chat")
async def chat():
    async def wrap():
        async for msg in gen():
            yield SSE(msg)

    return EventSourceResponse(wrap())
