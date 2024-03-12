from threading import Thread
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


def run_threaded(func, *args, **kwargs):
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.start()


schedule.every(2).seconds.do(run_threaded, fun1)
schedule.every(2).seconds.do(run_threaded, fun2, "fun2")

logging.basicConfig(level=logging.INFO)
print(f"{datetime.now().time()} ini")
while True:
    schedule.run_pending()
    time.sleep(1)
