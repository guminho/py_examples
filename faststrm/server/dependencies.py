from contextlib import asynccontextmanager

from fastapi import FastAPI
from worker.broker import broker
from worker.vectordb import connect_db, get_or_create_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.connect()
    app.state.broker = broker

    # Setup: initialize LanceDB for direct search access
    db = connect_db()
    app.state.md_chunks_table = get_or_create_table(db)

    yield
    await broker.stop()
