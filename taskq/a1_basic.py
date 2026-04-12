import asyncio
from time import monotonic

from taskiq import InMemoryBroker

broker = InMemoryBroker()
# Inmemory brokers cannot listen.


@broker.task
async def calc(x1: int) -> int:
    await asyncio.sleep(0.05)
    return x1 + 2


async def main() -> None:
    tik0 = monotonic()
    await broker.startup()

    tik1 = monotonic()
    task = await calc.kiq(x1=1)

    tik2 = monotonic()
    result = await task.wait_result(check_interval=0.1, timeout=2)
    if not result.is_err:
        print(f"Returned value: {result.return_value!r}")
    else:
        print("Error found while executing task.")

    tik3 = monotonic()
    await broker.shutdown()

    tik4 = monotonic()

    print(f"Task execution took: {result.execution_time:.3f} seconds.")
    print(f"Broker startup took: {tik1 - tik0:.3f} seconds.")
    print(f"Task creation took: {tik2 - tik1:.3f} seconds.")
    print(f"Task result retrieval took: {tik3 - tik2:.3f} seconds.")
    print(f"Broker shutdown took: {tik4 - tik3:.3f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
