from fastapi import FastAPI

app = FastAPI()


@app.get("/hello/{num}")
async def hello(num: int):
    return {"value": num + 1}
