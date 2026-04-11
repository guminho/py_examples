# broker.py
import asyncio

from taskiq_redis import RedisAsyncResultBackend, RedisStreamBroker

broker = RedisStreamBroker(
    url="redis://localhost:6379",
    queue_name="taskq0",
).with_result_backend(
    result_backend=RedisAsyncResultBackend(
        "redis://localhost:6379",
        result_ex_time=300,
    )
)


@broker.task(timeout=1.0, label2="math")
async def add_op(a: int, b: int) -> int:
    await asyncio.sleep(0.2)
    return a + b


async def main() -> None:
    await broker.startup()

    task = await add_op.kicker().kiq(1, 2)
    result = await task.wait_result(timeout=2)
    print(f"Task execution took: {result.execution_time} seconds.")
    if not result.is_err:
        print(f"Returned value: {result.return_value}")
    else:
        print("Error found while executing task.")

    await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
