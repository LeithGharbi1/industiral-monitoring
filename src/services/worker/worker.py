import json
import time

from src.core.db import get_connection, release_connection
from src.shared.database.redis_client import get_redis_client
from src.core.logger import get_logger
from src.core.config import settings

logger = get_logger("worker")

redis_client = None
QUEUE_NAME = settings.QUEUE_NAME


def safe_sleep(attempt: int):
    time.sleep(min(5 * attempt, 30))


def worker():
    global redis_client
    redis_client = get_redis_client()

    logger.info("Worker started")
    logger.info(f"Redis host={settings.REDIS_HOST} port={settings.REDIS_PORT}")
    logger.info(f"Queue={QUEUE_NAME}")

    attempt = 0

    while True:
        conn = None
        cursor = None
        request_id = None

        try:
            item = redis_client.blpop(QUEUE_NAME, timeout=5)

            if not item:
                continue

            _, raw_event = item
            event = json.loads(raw_event)
            request_id = event.get("request_id")

            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO machine_events (
                    id_machine, machine_type, line_id, timestamp, shift,
                    production_order_id, cycle_time, units_produced,
                    units_ok, units_nok, defect_code, defect_category,
                    downtime, downtime_reason, temperature,
                    vibration_level, operator_id
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    event.get("id_machine"),
                    event.get("machine_type"),
                    event.get("line_id"),
                    event.get("timestamp"),
                    event.get("shift"),
                    event.get("production_order_id"),
                    event.get("cycle_time"),
                    event.get("units_produced"),
                    event.get("units_ok"),
                    event.get("units_nok"),
                    event.get("defect_code"),
                    event.get("defect_category"),
                    event.get("downtime"),
                    event.get("downtime_reason"),
                    event.get("temperature"),
                    event.get("vibration_level"),
                    event.get("operator_id"),
                ),
            )

            conn.commit()
            logger.info(f"inserted machine={event.get('id_machine')} request_id={request_id}")

        except Exception as e:
            logger.error(f"worker_error request_id={request_id} error={repr(e)}")

            if conn:
                conn.rollback()
            logger.warning("retrying after error...")
            time.sleep(2)  # small fixed backoff (replace exponential chaos)

        finally:
            if cursor:
                cursor.close()
            if conn:
                release_connection(conn)
                
if __name__ == "__main__":
    worker()