import asyncio

from faststream.redis import RedisBroker


async def main():
    broker = RedisBroker("redis://localhost:6379")

    @broker.subscriber("test-stream")
    async def handler(msg):
        print(f"Received: {msg}")

    print("Connecting...")
    await broker.connect()
    print("Connected.")

    print("Publishing...")
    await broker.publish("hello", stream="test-stream")
    print("Published.")

    # Wait a bit to see if handler is called
    await asyncio.sleep(1)

    print("Stopping...")
    await broker.close()
    print("Stopped.")


if __name__ == "__main__":
    asyncio.run(main())
