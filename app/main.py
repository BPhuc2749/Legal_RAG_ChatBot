from fastapi import FastAPI
from app.api import router
from app.core.middleware import RequestContextMiddleware

app = FastAPI(
    title="Legal GenAI Assistant",
    version="0.1.0",
)

app.add_middleware(RequestContextMiddleware)
app.include_router(router)
