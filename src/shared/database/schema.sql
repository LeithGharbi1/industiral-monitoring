CREATE TABLE machine_events (
    id SERIAL PRIMARY KEY,
    id_machine VARCHAR(10),
    machine_type VARCHAR(50),
    line_id VARCHAR(10),
    timestamp TIMESTAMP,
    shift VARCHAR(5),

    production_order_id VARCHAR(20),

    cycle_time FLOAT,

    units_produced INT,
    units_ok INT,
    units_nok INT,

    defect_code VARCHAR(10),
    defect_category VARCHAR(50),

    downtime INT,
    downtime_reason VARCHAR(100),

    temperature FLOAT,
    vibration_level FLOAT,

    operator_id VARCHAR(10)
);