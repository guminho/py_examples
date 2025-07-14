import asyncio
from datetime import timedelta

from aiohttp_sse_client2.client import EventSource


async def main():
    url = "http://localhost:8000/chat"
    params = {"name": "world"}
    event_source = EventSource(
        url=url,
        option=dict(method="POST"),
        params=params,
        reconnection_time=timedelta(seconds=0.2),
    )
    async with event_source:
        async for sse in event_source:
            print(sse.data, sse.message)


asyncio.run(main())
