import asyncio
import os
import sys

import redis_client
from redis.exceptions import ResponseError

# Configuration
STREAM_NAME = "mystream"
GROUP_NAME = "mygroup"
# Get consumer name from CLI arg or generate one
CONSUMER_NAME = sys.argv[1] if len(sys.argv) > 1 else f"worker-{os.getpid()}"


async def process_message(message_id, data):
    print(f"[{CONSUMER_NAME}] Processing message {message_id}: {data}")
    # Fake work: sleep for 5 seconds
    await asyncio.sleep(5)
    print(f"[{CONSUMER_NAME}] Finished processing {message_id}")


async def main():
    print(f"[{CONSUMER_NAME}] Starting consumer...")
    r = await redis_client.init()

    # 1. Ensure the stream and consumer group exist
    try:
        # MKSTREAM will create the stream if it doesn't exist
        # '$' means we only care about new messages from now on
        await r.xgroup_create(STREAM_NAME, GROUP_NAME, id="$", mkstream=True)
        print(f"[{CONSUMER_NAME}] Consumer group '{GROUP_NAME}' created.")
    except ResponseError as e:
        if "BUSYGROUP" in str(e):
            print(f"[{CONSUMER_NAME}] Consumer group '{GROUP_NAME}' already exists.")
        else:
            raise

    check_pending = True
    print(f"[{CONSUMER_NAME}] Entering pending recovery state...")

    try:
        while True:
            if check_pending:
                # 2. Check for pending messages (ID '0')
                # These are messages delivered to THIS consumer but not acknowledged
                response = await r.xreadgroup(
                    GROUP_NAME, CONSUMER_NAME, {STREAM_NAME: "0"}, count=1
                )

                if not response:
                    print(
                        f"[{CONSUMER_NAME}] Pending list empty. Switching to listening state."
                    )
                    check_pending = False
                    continue
                else:
                    print(f"[{CONSUMER_NAME}] Found pending message. Recovering...")
            else:
                # 3. Read NEW messages (ID '>')
                # Use BLOCK to wait for new data efficiently
                response = await r.xreadgroup(
                    GROUP_NAME, CONSUMER_NAME, {STREAM_NAME: ">"}, count=1, block=5000
                )

            if response:
                # Response format: [[stream_name, [[message_id, data]]]]
                for stream, messages in response:
                    for message_id, data in messages:
                        await process_message(message_id, data)
                        # 4. ACK the message
                        await r.xack(STREAM_NAME, GROUP_NAME, message_id)
                        print(f"[{CONSUMER_NAME}] Acknowledged message {message_id}")

            await asyncio.sleep(0.1)  # Prevent tight loop if something goes wrong

    except asyncio.CancelledError:
        print(f"[{CONSUMER_NAME}] Stopping...")
    finally:
        await redis_client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
