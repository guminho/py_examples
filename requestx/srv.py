import asyncio

from fastapi import FastAPI

app = FastAPI()


@app.get("/hello/{num}")
async def hello(num: int):
    await asyncio.sleep(0.01)  # mock
    return {"value": num + 1}
