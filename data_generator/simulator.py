import os
import random
import time
from datetime import datetime
import requests
# -----------------------------
# CONFIGURATION
# -----------------------------

MACHINES = [
    {"id": "M1", "type": "Injection", "line": "L1"},
    {"id": "M2", "type": "Packaging", "line": "L1"},
    {"id": "M3", "type": "Assembly", "line": "L2"}
]

OPERATORS = ["OP1", "OP2", "OP3", "OP4"]

DEFECT_CODES = ["NONE", "D1", "D2", "D3"]

OUTPUT_FILE = "data-lake/raw/machine_data.csv"

SHIFTS = ["A", "B", "C"]

# -----------------------------
# CORE LOGIC
# -----------------------------

def generate_cycle_time():
    return round(random.uniform(5, 15), 2)


def generate_production():
    return random.randint(5, 20)


def generate_quality(units):
    defect_ratio = random.uniform(0, 0.3)

    units_nok = int(units * defect_ratio)
    units_ok = units - units_nok

    return units_ok, units_nok


def generate_defect():
    weights = [0.7, 0.1, 0.1, 0.1]
    code = random.choices(DEFECT_CODES, weights=weights)[0]
    return code


def generate_environment():
    return {
        "temperature": round(random.uniform(60, 90), 2),
        "vibration": round(random.uniform(0.1, 1.0), 2)
    }


def generate_downtime():
    return 1 if random.random() < 0.05 else 0


def generate_event():
    machine = random.choice(MACHINES)
    units = generate_production()
    ok, nok = generate_quality(units)
    env = generate_environment()

    return {
        "id_machine": machine["id"],
        "machine_type": machine["type"],
        "line_id": machine["line"],

        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "shift": random.choice(SHIFTS),
        "production_order_id": f"PO{random.randint(1000,9999)}",

        "cycle_time": generate_cycle_time(),

        "units_produced": units,
        "units_ok": ok,
        "units_nok": nok,

        "defect_code": generate_defect(),
        "defect_category": "mechanical",

        "downtime": generate_downtime(),
        "downtime_reason": None,

        "temperature": env["temperature"],
        "vibration_level": env["vibration"],

        "operator_id": random.choice(OPERATORS)
    }


# -----------------------------
# STREAMING ENGINE
# -----------------------------

API_URL = os.getenv("API_URL", "http://ingestion:8000/ingest")

def stream_data(interval=2):
    print("Streaming to FastAPI ingestion layer...")

    while True:
        event = generate_event()

        try:
            response = requests.post(API_URL, json=event, timeout=5)

            if response.status_code == 200:
                print("sent ✔")
            else:
                print("failed:", response.text)
        except requests.exceptions.RequestException as e:
            print("ingestion not ready:", e)

        time.sleep(interval)


# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    stream_data(interval=2)