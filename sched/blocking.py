import logging
import schedule
import time
from datetime import datetime


def fun1():
    print(f"{datetime.now().time()} fun1 ini")
    time.sleep(3)
    print(f"{datetime.now().time()} fun1 end")


def fun2():
    print(f"{datetime.now().time()} fun2 end")


schedule.every(2).seconds.do(fun1)
schedule.every(2).seconds.do(fun2)

logging.basicConfig(level=logging.INFO)
print(f"{datetime.now().time()} ini")
while True:
    schedule.run_pending()
    time.sleep(1)
