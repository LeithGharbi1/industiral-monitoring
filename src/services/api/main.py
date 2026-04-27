from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException

from src.core.db import get_connection
from src.shared.database.redis_client import get_redis_client
from src.core.logger import get_logger
from src.shared.schemas.machine_event import MachineEvent

logger = get_logger("ingestion")

QUEUE_NAME = "machine_events"
redis_client = None


# -------------------------
# LIFESPAN (SAFE INIT)
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client

    try:
        redis_client = get_redis_client()
        redis_client.ping()
        logger.info("Redis connected")
    except Exception as e:
        logger.exception(f"Redis init failed: {e}")
        redis_client = None

    logger.info("API started")
    yield
    logger.info("API shutting down")


app = FastAPI(
    title="Industrial Data Ingestion API",
    lifespan=lifespan
)


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health")
def health():
    db_status = "down"
    redis_status = "down"

    # DB check
    try:
        conn = get_connection()
        conn.close()
        db_status = "connected"
    except Exception as e:
        logger.warning(f"DB check failed: {e}")

    # Redis check
    try:
        if redis_client:
            redis_client.ping()
            redis_status = "connected"
    except Exception as e:
        logger.warning(f"Redis check failed: {e}")

    return {
        "status": "healthy" if db_status == "connected" and redis_status == "connected" else "degraded",
        "db": db_status,
        "redis": redis_status
    }


# -------------------------
# INGEST ENDPOINT
# -------------------------
@app.post("/ingest")
def ingest_event(event: MachineEvent):

    if not redis_client:
        logger.error("Redis not initialized")
        raise HTTPException(status_code=503, detail="Redis not available")

    try:
        payload = event.model_dump_json()

        redis_client.rpush(QUEUE_NAME, payload)

        logger.info(
            f"queued_event machine={event.id_machine}"
        )

        return {"status": "queued"}

    except Exception as e:
        logger.exception(f"redis_enqueue_error: {repr(e)}")
        raise HTTPException(status_code=500, detail="Queue error")