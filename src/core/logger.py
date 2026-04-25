import logging
import json
import sys
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log = {
            "time": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.name,
        }

        # attach request_id if exists
        if hasattr(record, "request_id"):
            log["request_id"] = record.request_id

        return json.dumps(log)


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    if not logger.handlers:
        logger.addHandler(handler)

    return logger