import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from time import monotonic

import aiohttp
import httpx
import niquests
import pycurl_requests
import requests
import urllib3

URL = "http://localhost:8000/hello/{num}"
NUM_REQUESTS = 60
REPEAT = 5

_pycurl_thread_local = threading.local()


def get_pycurl_session():
    if not hasattr(_pycurl_thread_local, "sess"):
        _pycurl_thread_local.sess = pycurl_requests.Session()
    return _pycurl_thread_local.sess


def benchmark_sync(name, sess, run_func):
    with ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
        tik = monotonic()
        for _ in range(REPEAT):
            list(executor.map(lambda n: run_func(sess, n), range(NUM_REQUESTS)))
        tok = monotonic()
        print(f"{name:<20}: {tok - tik:.3f}s")


async def benchmark_async(name, sess, run_func):
    tik = monotonic()
    for _ in range(REPEAT):
        tasks = [run_func(sess, n) for n in range(NUM_REQUESTS)]
        await asyncio.gather(*tasks)
    tok = monotonic()
    print(f"{name:<20}: {tok - tik:.3f}s")


def test_requests_sync():
    def run(sess: requests.Session, num) -> bytes:
        return sess.get(URL.format(num=num)).content

    with requests.Session() as sess:
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=NUM_REQUESTS, pool_maxsize=NUM_REQUESTS
        )
        sess.mount("http://", adapter)
        sess.mount("https://", adapter)
        benchmark_sync("Requests (Sync)", sess, run)


def test_httpx_sync():
    def run(sess: httpx.Client, num) -> bytes:
        return sess.get(URL.format(num=num)).content

    with httpx.Client() as sess:
        benchmark_sync("HTTPX (Sync)", sess, run)


def test_urllib3_sync():
    def run(sess: urllib3.PoolManager, num) -> bytes:
        return sess.request("GET", URL.format(num=num)).data

    sess = urllib3.PoolManager(maxsize=NUM_REQUESTS)
    benchmark_sync("Urllib3 (Sync)", sess, run)


def test_niquests_sync():
    def run(sess: niquests.Session, num) -> bytes:
        return sess.get(URL.format(num=num)).content

    with niquests.Session(
        pool_connections=NUM_REQUESTS, pool_maxsize=NUM_REQUESTS
    ) as sess:
        benchmark_sync("Niquests (Sync)", sess, run)


def test_pycurl_sync():
    def run(_, num) -> bytes:
        sess = get_pycurl_session()
        return sess.get(URL.format(num=num)).content

    benchmark_sync("Pycurl-Req (Sync)", None, run)


async def test_httpx_async():
    async def run(sess: httpx.AsyncClient, num) -> bytes:
        res = await sess.get(URL.format(num=num))
        return res.content

    async with httpx.AsyncClient() as sess:
        await benchmark_async("HTTPX (Async)", sess, run)


async def test_aiohttp_async():
    async def run(sess: aiohttp.ClientSession, num) -> bytes:
        async with sess.get(URL.format(num=num)) as res:
            return await res.read()

    async with aiohttp.ClientSession() as sess:
        await benchmark_async("Aiohttp (Async)", sess, run)


def main():
    print(f"Benchmarking {NUM_REQUESTS} requests...")
    # Run sync tests
    test_requests_sync()
    test_niquests_sync()
    test_httpx_sync()
    test_urllib3_sync()
    test_pycurl_sync()

    # Run async tests
    asyncio.run(test_httpx_async())
    asyncio.run(test_aiohttp_async())


if __name__ == "__main__":
    main()
