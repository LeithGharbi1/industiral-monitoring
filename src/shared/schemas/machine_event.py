from pydantic import BaseModel
from typing import Optional


class MachineEvent(BaseModel):
    request_id: str | None = None
    id_machine: str
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
    downtime_reason: Optional[str]

    temperature: float
    vibration_level: float

    operator_id: str