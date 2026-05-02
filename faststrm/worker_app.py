# Import tasks so subscribers get registered on the broker
import worker.tasks  # noqa: F401
from contextlib import asynccontextmanager

from faststream import ContextRepo, FastStream
from faststream.specification import AsyncAPI

from worker.broker import broker


@asynccontextmanager
async def lifespan(context: ContextRepo):
    # Setup: initialize per-user counters
    greeting_counter: dict[str, int] = {}
    goodbye_counter: dict[str, int] = {}
    context.set_global("greeting_counter", greeting_counter)
    context.set_global("goodbye_counter", goodbye_counter)
    yield
    # Teardown: clean up resources after broker stops
    greeting_counter.clear()
    goodbye_counter.clear()


app = FastStream(broker, lifespan=lifespan, specification=AsyncAPI())
