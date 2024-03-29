import asyncio

import orjson
from httpx import AsyncClient
from httpx_sse import aconnect_sse


async def main():
    client = AsyncClient(base_url="http://localhost:8000")
    params = {"name": "world"}
    async with aconnect_sse(
        url="/",
        method="POST",
        params=params,
        client=client,
    ) as event_source:
        async for sse in event_source.aiter_sse():
            if sse.data.startswith("[DONE]"):
                break
            else:
                print("data:", [orjson.loads(sse.data)])


asyncio.run(main())
