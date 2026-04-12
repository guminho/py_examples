import asyncio

from taskiq_nats import NATSObjectStoreResultBackend, PullBasedJetStreamBroker

broker = PullBasedJetStreamBroker(
    servers=["nats://localhost:4222"],
    queue="taskq0",
).with_result_backend(
    result_backend=NATSObjectStoreResultBackend(
        servers=["nats://localhost:4222"],
        bucket_name="taskq0_results",
    )
)


@broker.task
async def calc(x1: int) -> int:
    await asyncio.sleep(0.05)
    return x1 + 2


async def main() -> None:
    await broker.startup()

    task = await calc.kiq(x1=1)
    result = await task.wait_result(timeout=2)
    if not result.is_err:
        print(f"Returned value: {result.return_value!r}")
    else:
        print("Error found while executing task.")

    await broker.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
