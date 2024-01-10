import asyncio
import logging

import orjson
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse, ServerSentEvent

_logger = logging.getLogger(__name__)
app = FastAPI()


async def gen(name: str):
    for i in range(10):
        await asyncio.sleep(0.2)
        yield dict(hello=f"{name}-{i}")


@app.post("/")
async def hello(name: str):
    async def _stream():
        try:
            async for data in gen(name):
                yield ServerSentEvent(orjson.dumps(data).decode(), event="data")
            yield ServerSentEvent(event="end")
        except BaseException as exc:
            _logger.error("stream error", exc_info=exc)

    return EventSourceResponse(_stream())
