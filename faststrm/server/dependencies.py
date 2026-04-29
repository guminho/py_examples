from contextlib import asynccontextmanager

from fastapi import FastAPI
from worker.broker import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    app.state.broker = broker
    yield
    await broker.close()
