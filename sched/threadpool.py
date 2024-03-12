from concurrent.futures import ThreadPoolExecutor
import logging
import schedule
import time
from datetime import datetime


def fun1():
    print(f"{datetime.now().time()} fun1 ini")
    time.sleep(3)
    print(f"{datetime.now().time()} fun1 end")


def fun2(label):
    print(f"{datetime.now().time()} {label} end")


pool = ThreadPoolExecutor(2)


def run_threaded(func, *args, **kwargs):
    pool.submit(func, *args, **kwargs)


schedule.every(2).seconds.do(run_threaded, fun1)
schedule.every(2).seconds.do(run_threaded, fun2, "fun2")

logging.basicConfig(level=logging.INFO)
print(f"{datetime.now().time()} ini")
while True:
    schedule.run_pending()
    time.sleep(1)
