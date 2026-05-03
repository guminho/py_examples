# Import tasks so subscribers get registered on the broker
from contextlib import asynccontextmanager

import worker.ingest  # noqa: F401
import worker.tasks  # noqa: F401
from faststream import ContextRepo, FastStream
from faststream.specification import AsyncAPI
from worker.broker import broker
from worker.vectordb import connect_db, get_or_create_table


@asynccontextmanager
async def lifespan(context: ContextRepo):
    # Setup: initialize per-user counters
    greeting_counter: dict[str, int] = {}
    goodbye_counter: dict[str, int] = {}
    context.set_global("greeting_counter", greeting_counter)
    context.set_global("goodbye_counter", goodbye_counter)

    # Setup: initialize LanceDB
    db = connect_db()
    md_chunks_table = get_or_create_table(db)
    context.set_global("md_chunks_table", md_chunks_table)

    yield
    # Teardown: clean up resources after broker stops
    greeting_counter.clear()
    goodbye_counter.clear()


app = FastStream(broker, lifespan=lifespan, specification=AsyncAPI())
