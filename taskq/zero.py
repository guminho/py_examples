import asyncio

from taskiq import ZeroMQBroker
from taskiq_redis import RedisAsyncResultBackend

result_backend = RedisAsyncResultBackend(
    "redis://localhost:6379",
    result_ex_time=300,
)
broker = ZeroMQBroker().with_result_backend(
    result_backend=result_backend,
)


@broker.task
def calc(x1: int) -> int:
    return x1 + 2


async def main() -> None:
    await broker.startup()
    # ZeroMQ PUB/SUB needs a moment to handshake before publishing.
    await asyncio.sleep(1)

    task = await calc.kiq(x1=1)
    result = await task.wait_result(check_interval=0.1, timeout=2)
    if not result.is_err:
        print(f"Returned value: {result.return_value}")
    else:
        print("Error found while executing task.")

    await result_backend.shutdown()
    await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
