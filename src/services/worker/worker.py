import json
import time

from src.shared.database.db import get_connection, release_connection
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
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    event["id_machine"],
                    event["machine_type"],
                    event["line_id"],
                    event["timestamp"],
                    event["shift"],
                    event["production_order_id"],
                    event["cycle_time"],
                    event["units_produced"],
                    event["units_ok"],
                    event["units_nok"],
                    event["defect_code"],
                    event["defect_category"],
                    event["downtime"],
                    event["downtime_reason"],
                    event["temperature"],
                    event["vibration_level"],
                    event["operator_id"],
                ),
            )

            conn.commit()
            logger.info(f"inserted machine={event['id_machine']} request_id={request_id}")

            attempt = 0

        except Exception as e:
            logger.error(f"worker_error request_id={request_id} error={repr(e)}")

            if conn:
                conn.rollback()

            attempt += 1
            safe_sleep(attempt)

        finally:
            if cursor:
                cursor.close()
            if conn:
                release_connection(conn)
                
if __name__ == "__main__":
    worker()