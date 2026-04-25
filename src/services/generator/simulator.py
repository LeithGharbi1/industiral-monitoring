import os
import random
import time
from datetime import datetime
import requests
from src.core.logger import get_logger
import uuid
# -----------------------------
# LOGGING
# -----------------------------

logger = get_logger("generator")

# -----------------------------
# CONFIGURATION
# -----------------------------
API_URL = os.getenv("API_URL")

MACHINES = [
    {"id": "M1", "type": "Injection", "line": "L1"},
    {"id": "M2", "type": "Packaging", "line": "L1"},
    {"id": "M3", "type": "Assembly", "line": "L2"}
]

OPERATORS = ["OP1", "OP2", "OP3", "OP4"]
DEFECT_CODES = ["NONE", "D1", "D2", "D3"]
SHIFTS = ["A", "B", "C"]

# -----------------------------
# GENERATION LOGIC
# -----------------------------
def generate_cycle_time():
    return round(random.uniform(5, 15), 2)

def generate_production():
    return random.randint(5, 20)

def generate_quality(units):
    defect_ratio = random.uniform(0, 0.3)
    units_nok = int(units * defect_ratio)
    return units - units_nok, units_nok

def generate_defect():
    weights = [0.7, 0.1, 0.1, 0.1]
    return random.choices(DEFECT_CODES, weights=weights)[0]

def generate_environment():
    return {
        "temperature": round(random.uniform(60, 90), 2),
        "vibration": round(random.uniform(0.1, 1.0), 2)
    }

def generate_event():
    machine = random.choice(MACHINES)
    units = generate_production()
    ok, nok = generate_quality(units)
    env = generate_environment()

    return {
        "request_id": str(uuid.uuid4()),
        "id_machine": machine["id"],
        "machine_type": machine["type"],
        "line_id": machine["line"],
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "shift": random.choice(SHIFTS),
        "production_order_id": f"PO{random.randint(1000,9999)}",
        "cycle_time": generate_cycle_time(),
        "units_produced": units,
        "units_ok": ok,
        "units_nok": nok,
        "defect_code": generate_defect(),
        "defect_category": "mechanical",
        "downtime": 1 if random.random() < 0.05 else 0,
        "downtime_reason": None,
        "temperature": env["temperature"],
        "vibration_level": env["vibration"],
        "operator_id": random.choice(OPERATORS)
    }

# -----------------------------
# STREAMING ENGINE
# -----------------------------
def stream_data(interval=2):
    logger.info(f"Streaming started → {API_URL}")

    while True:
        event = generate_event()

        success = False
        retries = 3

        while retries > 0 and not success:
            try:
                response = requests.post(API_URL, json=event, timeout=5)

                if response.status_code == 200:
                    logger.info("sent ✔")
                    success = True
                else:
                    logger.warning(
                        f"failed {response.status_code}: {response.text}"
                    )

            except requests.exceptions.RequestException as e:
                logger.error(f"request error: {str(e)}")

            retries -= 1
            if not success:
                time.sleep(1)

        time.sleep(interval)

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    stream_data(interval=2)