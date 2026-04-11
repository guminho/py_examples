# broker.py
import asyncio
import random
from typing import Annotated

from taskiq import InMemoryBroker, TaskiqDepends

broker = InMemoryBroker()


@broker.task
async def add_one(value: int) -> int:
    return value + 1


def common_dep() -> int:
    # For example it returns 8
    return random.randint(1, 10)


def dep1(cd: Annotated[int, TaskiqDepends(common_dep)]) -> int:
    # This function will return 9
    return cd + 1


def dep2(cd: Annotated[int, TaskiqDepends(common_dep, use_cache=False)]) -> int:
    # This function will return 10
    return cd + 2


@broker.task
def my_task(
    d1: Annotated[int, TaskiqDepends(dep1)],
    d2: Annotated[int, TaskiqDepends(dep2)],
) -> tuple[int, int]:
    # This function will return (9, 10)
    return d1, d2


async def main() -> None:
    await broker.startup()

    task = await add_one.kiq(1)
    result = await task.wait_result(timeout=2)
    print(f"Task execution took: {result.execution_time} seconds.")
    if not result.is_err:
        print(f"Returned value: {result.return_value!r}")
    else:
        print("Error found while executing task.")

    task = await my_task.kiq()
    result = await task.wait_result(timeout=2)
    print(f"Task execution took: {result.execution_time} seconds.")
    if not result.is_err:
        print(f"Returned value: {result.return_value!r}")
    else:
        print("Error found while executing task.")

    await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
