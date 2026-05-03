from fastapi import FastAPI
from server.dependencies import lifespan
from server.routes import router
from server.search import router as search_router
from server.upload import router as upload_router

app = FastAPI(title="FastStream Publisher", lifespan=lifespan)
app.include_router(router)
app.include_router(upload_router)
app.include_router(search_router)
