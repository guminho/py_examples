from faststream import Context, Logger
from faststream.redis import StreamSub

from worker.broker import broker
from worker.constants import (
    CONSUMER_NAME,
    GOODBYE_GROUP,
    GOODBYE_STREAM,
    GREETING_GROUP,
    GREETING_STREAM,
)
from worker.models import GoodbyeMessage, GreetingMessage


@broker.subscriber(
    stream=StreamSub(GREETING_STREAM, group=GREETING_GROUP, consumer=CONSUMER_NAME)
)
async def handle_greeting(
    msg: GreetingMessage, logger: Logger, greeting_counter: dict = Context()
):
    greeting_counter[msg.user_name] = greeting_counter.get(msg.user_name, 0) + 1
    logger.info(
        f"👋 Hello, {msg.user_name} (id={msg.user_id})! Greeting count: {greeting_counter[msg.user_name]}"
    )


@broker.subscriber(
    stream=StreamSub(GOODBYE_STREAM, group=GOODBYE_GROUP, consumer=CONSUMER_NAME)
)
async def handle_goodbye(
    msg: GoodbyeMessage, logger: Logger, goodbye_counter: dict = Context()
):
    goodbye_counter[msg.user_name] = goodbye_counter.get(msg.user_name, 0) + 1
    logger.info(
        f"👋 Goodbye, {msg.user_name} (id={msg.user_id})! Goodbye count: {goodbye_counter[msg.user_name]}"
    )
