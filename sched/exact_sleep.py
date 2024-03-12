import logging
import schedule
import time
from datetime import datetime


def fun1():
    print(f"{datetime.now().time()} fun1")


def fun2():
    print(f"{datetime.now().time()} fun2")


schedule.every(2).seconds.do(fun1)
schedule.every(3).seconds.do(fun2)

logging.basicConfig(level=logging.INFO)
print(f"{datetime.now().time()} ini")
while True:
    n = schedule.idle_seconds()
    if n is None:
        break
    elif n > 0:
        time.sleep(n)
    schedule.run_pending()
