from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from src.shared.database.db import get_connection
from src.shared.database.redis_client import get_redis_client
from src.core.logger import get_logger
from src.shared.schemas.machine_event import MachineEvent

logger = get_logger("ingestion")

QUEUE_NAME = "machine_events"

redis_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_client = get_redis_client()
    logger.info("API started")
    yield
    logger.info("API shutting down")


app = FastAPI(
    title="Industrial Data Ingestion API",
    lifespan=lifespan
)


@app.get("/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "healthy", "db": "connected"}
    except Exception:
        return {"status": "unhealthy", "db": "down"}


@app.post("/ingest")
def ingest_event(event: MachineEvent):

    try:
        redis_client.rpush(
            QUEUE_NAME,
            event.model_dump_json()
        )

        logger.info(f"queued_event machine={event.id_machine} request_id={getattr(event, 'request_id', None)}")

        return {"status": "queued"}

    except Exception as e:
        logger.exception(f"redis_enqueue_error: {repr(e)}")
        raise HTTPException(status_code=500, detail="Queue error")