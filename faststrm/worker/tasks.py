from faststream import Logger

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
async def handle_greeting(msg: GreetingMessage, logger: Logger):
    logger.info(f"👋 Hello, {msg.user_name} (id={msg.user_id})!")


@broker.subscriber(
    stream=StreamSub(GOODBYE_STREAM, group=GOODBYE_GROUP, consumer=CONSUMER_NAME)
)
async def handle_goodbye(msg: GoodbyeMessage, logger: Logger):
    logger.info(f"👋 Goodbye, {msg.user_name} (id={msg.user_id})!")
