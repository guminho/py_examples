import asyncio

import orjson
from httpx import AsyncClient
from httpx_sse import aconnect_sse

client = AsyncClient(base_url="http://localhost:8000")


async def main():
    params = {"name": "world"}
    async with aconnect_sse(client, "POST", "/", params=params) as event_source:
        async for sse in event_source.aiter_sse():
            if sse.event == "end":
                break
            elif sse.event == "data":
                print("data:", [orjson.loads(sse.data)])
            else:
                print("unsupported event:", [sse])


asyncio.run(main())
