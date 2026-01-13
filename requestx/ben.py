import asyncio
from time import monotonic

import aiohttp
import geventhttpclient
import httpx
import niquests
import pycurl_requests
import requests
import urllib3

NUM = 1000
URL = "http://localhost:8000/hello/10"
TMP = "{:11}:{:<7}:{}"


def test(name, make_sess, runner, num=2):
    with make_sess() as sess:
        tik = monotonic()
        for _ in range(num):
            out = runner(sess)
        tok = monotonic()
    print(TMP.format(name, round(tok - tik, 2), out))


async def atest(name, make_sess, runner, num=2):
    async with make_sess() as sess:
        tik = monotonic()
        for _ in range(num):
            out = await runner(sess)
        tok = monotonic()
    print(TMP.format(name, round(tok - tik, 2), out))


def request_run(sess: requests.Session) -> bytes:
    res = sess.get(URL)
    return res.content


def httpx_run(sess: httpx.Client) -> bytes:
    res = sess.get(URL)
    return res.content


def urllib3_run(sess: urllib3.PoolManager) -> bytes:
    res = sess.request("GET", URL)
    return res.data


def niquest_run(sess: niquests.Session) -> bytes:
    res = sess.get(URL)
    return res.content


def pycurl_run(sess: pycurl_requests.Session):
    res = sess.get(URL)
    return res.content


def geventcli_run(sess: geventhttpclient.Session):
    res = sess.get(URL)
    return res.data


async def httpx_arun(sess: httpx.AsyncClient):
    res = await sess.get(URL)
    return res.content


async def aiohttp_run(sess: aiohttp.ClientSession) -> bytes:
    res = await sess.get(URL)
    return await res.read()


async def run():
    test("req", requests.Session, request_run, NUM)
    test("niquest", niquests.Session, niquest_run, NUM)
    test("httpx", httpx.Client, httpx_run, NUM)
    test("urllib3", urllib3.PoolManager, urllib3_run, NUM)
    test("pycurl", pycurl_requests.Session, pycurl_run, NUM)
    test("gevent-cli", geventhttpclient.Session, geventcli_run, NUM)
    await atest("httpx-aio", httpx.AsyncClient, httpx_arun, NUM)
    await atest("aiohttp", aiohttp.ClientSession, aiohttp_run, NUM)


asyncio.run(run())
