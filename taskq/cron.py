from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisStreamBroker

broker = RedisStreamBroker(
    url="redis://localhost:6379/0",
    queue_name="taskq1",
)

cron_src = LabelScheduleSource(broker)
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[cron_src],
)


@broker.task(schedule=[{"cron": "*/1 * * * *", "args": [1]}])
async def heavy_task(value: int) -> int:
    return value + 1
