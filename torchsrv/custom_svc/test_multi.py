import asyncio
import json
from time import monotonic

from httpx import AsyncClient

cli = AsyncClient()
URL = "http://localhost:8080/predictions/grt"


async def pred(bar: str):
    resp = await cli.post(URL, data={"body": json.dumps({"foo": bar})})
    print(resp.elapsed)
    return resp.text


async def main():
    tik = monotonic()
    resps = await asyncio.gather(*[pred(f"bar{i}") for i in range(10)])
    tok = monotonic()
    print("resps:", resps)
    print("elapsed:", tok - tik)


asyncio.run(main())
