import json
import logging
import os
from datetime import datetime, timezone

LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.getenv("LOG_FILE", "app.jsonl")


def get_jsonl_logger(name: str = "app") -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

  
    if logger.handlers:
        return logger

    path = os.path.join(LOG_DIR, LOG_FILE)
    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setLevel(logging.INFO)

 
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)

    return logger


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_event(logger: logging.Logger, event: dict) -> None:
    event.setdefault("ts", now_iso())
    logger.info(json.dumps(event, ensure_ascii=False))
