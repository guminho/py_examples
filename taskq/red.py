# broker.py
import asyncio
from typing import Annotated

from taskiq import Context, TaskiqDepends, TaskiqEvents, TaskiqState
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


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_startup(state: TaskiqState) -> None:
    state.mykey = "myvalue"
    print(f"Worker is starting up: {state=}")


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def on_shutdown(state: TaskiqState) -> None:
    print(f"Worker is shutting down: {state=}")


@broker.task(timeout=1.0, label2="math")
async def add_op(
    a: int,
    b: int,
    context: Annotated[Context, TaskiqDepends()],
) -> tuple[str, int]:  # type cast
    await asyncio.sleep(0.2)
    return context.state.mykey, str(a + b)


async def main() -> None:
    await broker.startup()

    task = await add_op.kiq(1, 2)
    result = await task.wait_result(timeout=2)
    print(f"Task execution took: {result.execution_time} seconds.")
    if not result.is_err:
        print(f"Returned value: {result.return_value!r}")
    else:
        print("Error found while executing task.")

    await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
