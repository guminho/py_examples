import asyncio
from datetime import timedelta

from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq.scheduler.scheduled_task import ScheduledTask
from taskiq_redis import RedisStreamBroker

broker = RedisStreamBroker(
    url="redis://localhost:6379/0",
    queue_name="taskq1",
)
schedule_source = LabelScheduleSource(
    broker=broker,
)
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[schedule_source],
)

schedule_heavy_task: ScheduledTask = {
    "interval": timedelta(seconds=5),
    # "cron": "* * * * *",
    "args": [5],
    "labels": {"mykey": "math"},
}


@broker.task(schedule=[schedule_heavy_task])
async def heavy_task(x1: int, x2: int = 2) -> int:
    await asyncio.sleep(0.05)
    print(x1 + x2)
