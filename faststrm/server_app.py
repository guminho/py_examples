from fastapi import FastAPI
from server.dependencies import lifespan
from server.routes import router

app = FastAPI(title="FastStream Publisher", lifespan=lifespan)
app.include_router(router)
