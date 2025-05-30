from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)


@app.get("/item1")
async def get_item1():
    return {"foo1": "bar1"}


@app.post("/item2")
async def post_item2():
    return {"foo2": "bar2"}
