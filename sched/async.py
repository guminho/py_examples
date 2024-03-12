import asyncio
import logging
import schedule
from datetime import datetime


async def fun1():
    print(f"{datetime.now().time()} fun1 ini")
    await asyncio.sleep(3)
    print(f"{datetime.now().time()} fun1 end")


async def fun2(label):
    print(f"{datetime.now().time()} {label} ini")
    await asyncio.sleep(3)
    print(f"{datetime.now().time()} {label} end")


loop = asyncio.get_event_loop()


def run_async(afunc, *args, **kwargs):
    loop.create_task(afunc(*args, **kwargs))


schedule.every(2).seconds.do(run_async, fun1)
schedule.every(2).seconds.do(run_async, fun2, "fun2")


async def main():
    logging.basicConfig(level=logging.INFO)
    print(f"{datetime.now().time()} ini")
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)


loop.run_until_complete(main())
