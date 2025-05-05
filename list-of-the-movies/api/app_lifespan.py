from typing import Generator

from crud.crud import storage

from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    storage.init_storage_from_state()
    yield
