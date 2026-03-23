import asyncio
from time import monotonic

import aiohttp

URL = "http://localhost:8000/hello/{num}"


async def request_run(sess: aiohttp.ClientSession, num: int):
    async with sess.get(URL.format(num=num)) as res:
        return await res.read()


async def test():
    nums = range(50)
    async with aiohttp.ClientSession() as sess:
        tik = monotonic()
        tasks = [request_run(sess, n) for n in nums]
        results = await asyncio.gather(*tasks)
        tok = monotonic()
        print(f"{tok - tik:.3f}s")

    for res in results[-3:]:
        print(res)


if __name__ == "__main__":
    asyncio.run(test())
