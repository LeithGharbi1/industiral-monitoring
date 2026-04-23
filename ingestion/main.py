import logging
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from database.db import get_connection

app = FastAPI(title="Industrial Data Ingestion API")

# -----------------------------
# LOGGING (STRUCTURED JSON)
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format='{"time":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
    stream=sys.stdout
)

logger = logging.getLogger(__name__)

# -----------------------------
# DATA MODEL (STRICT VALIDATION)
# -----------------------------
class MachineEvent(BaseModel):
    id_machine: str = Field(..., min_length=1)
    machine_type: str
    line_id: str
    timestamp: str
    shift: str
    production_order_id: str

    cycle_time: float

    units_produced: int
    units_ok: int
    units_nok: int

    defect_code: str
    defect_category: str

    downtime: int
    downtime_reason: str | None = None

    temperature: float
    vibration_level: float

    operator_id: str


# -----------------------------
# HEALTH CHECK ENDPOINT
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -----------------------------
# INGESTION ENDPOINT
# -----------------------------
@app.post("/ingest")
def ingest_event(event: MachineEvent):

    logger.info(f"Received event from machine={event.id_machine}")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO machine_events (
                id_machine,
                machine_type,
                line_id,
                timestamp,
                shift,
                production_order_id,
                cycle_time,
                units_produced,
                units_ok,
                units_nok,
                defect_code,
                defect_category,
                downtime,
                downtime_reason,
                temperature,
                vibration_level,
                operator_id
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            event.id_machine,
            event.machine_type,
            event.line_id,
            event.timestamp,
            event.shift,
            event.production_order_id,
            event.cycle_time,
            event.units_produced,
            event.units_ok,
            event.units_nok,
            event.defect_code,
            event.defect_category,
            event.downtime,
            event.downtime_reason,
            event.temperature,
            event.vibration_level,
            event.operator_id
        ))

        conn.commit()
        logger.info("Event inserted successfully")

    except Exception as e:
        logger.error(f"Database error: {str(e)}")

        if conn:
            conn.rollback()

        raise HTTPException(status_code=500, detail="Database error")

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return {"status": "success"}