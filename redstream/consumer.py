import asyncio
import os
import sys

import redis_client
from redis.exceptions import ResponseError

STREAM_NAME = "mystream"
GROUP_NAME = "mygroup"
CONSUMER_NAME = sys.argv[1] if len(sys.argv) > 1 else f"worker-{os.getpid()}"


async def process_message(message_id, data):
    print(f"[{CONSUMER_NAME}] Processing message {message_id}: {data}")
    await asyncio.sleep(5)  # simulate work
    print(f"[{CONSUMER_NAME}] Finished processing {message_id}")


async def ensure_consumer_group(r):
    """Create the consumer group, ignoring the error if it already exists."""
    try:
        # id="$" = only new messages; mkstream = create stream if absent
        await r.xgroup_create(STREAM_NAME, GROUP_NAME, id="$", mkstream=True)
        print(f"[{CONSUMER_NAME}] Consumer group '{GROUP_NAME}' created.")
    except ResponseError as e:
        if "BUSYGROUP" in str(e):
            print(f"[{CONSUMER_NAME}] Consumer group '{GROUP_NAME}' already exists.")
        else:
            raise


async def main():
    r = await redis_client.init()
    await ensure_consumer_group(r)

    # On the first pass read the backlog (pending messages for this consumer,
    # e.g. from a previous crash). Once the backlog is empty, switch to ">".
    last_id = "0-0"
    check_backlog = True
    print(f"[{CONSUMER_NAME}] Starting...")

    try:
        while True:
            stream_id = last_id if check_backlog else ">"

            items = await r.xreadgroup(
                groupname=GROUP_NAME,
                consumername=CONSUMER_NAME,
                streams={STREAM_NAME: stream_id},
                count=10,
                block=2000,
            )

            if not items:
                continue  # block timeout, loop again

            _, messages = items[0]

            if len(messages) == 0:
                # Empty reply during backlog scan means history is exhausted.
                check_backlog = False
                continue

            for msg_id, data in messages:
                await process_message(msg_id, data)
                await r.xack(STREAM_NAME, GROUP_NAME, msg_id)
                last_id = msg_id

    except asyncio.CancelledError:
        print(f"[{CONSUMER_NAME}] Stopping...")
    finally:
        await redis_client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
