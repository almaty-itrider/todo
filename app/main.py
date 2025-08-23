from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.settings import create_db_and_tables
from .routers import statuses, types


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield create_db_and_tables()


app = FastAPI(lifespan=lifespan)

origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(statuses.router)
app.include_router(types.router)
