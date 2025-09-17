import os
from contextlib import asynccontextmanager

import uvicorn
from api.exception_handlers import validation_exception_handler
from api.router import router
from config import init_whatever, settings
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from middlewares.logging import LogMiddleware
from pydantic import ValidationError


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_whatever()
    yield


app = FastAPI(title=settings.SERVICE_NAME, version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogMiddleware)

app.include_router(router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)


@app.get("/")
async def read_root():
    return {"message": f"{settings.SERVICE_NAME} service"}


# Note: A single Uvicorn worker is probably what you would want to use when using a distributed container management system like Kubernetes.
if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.HOST,
        port=settings.PORT,
        log_config=None,
        workers=max(1, os.cpu_count() - 1),
    )
