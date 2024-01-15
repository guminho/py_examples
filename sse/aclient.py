import asyncio

import orjson
from aiohttp import ClientSession
from aiohttp_sse_client2.client import EventSource


async def main():
    client = ClientSession("http://localhost:8000")
    params = {"name": "world"}
    async with EventSource(
        url="/",
        option=dict(method="POST"),
        params=params,
        session=client,
    ) as event_source:
        async for sse in event_source:
            if sse.data.startswith("[DONE]"):
                break
            else:
                print("data:", [orjson.loads(sse.data)])
    await client.close()


asyncio.run(main())
