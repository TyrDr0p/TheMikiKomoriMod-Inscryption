from __future__ import annotations

import json
import logging
import re
import sys
from pathlib import Path

from jsonschema import validators


logger = logging.getLogger(__name__)

SCHEMA_FILES = {
    "cards": "cards.schema.json",
    "sigils": "sigils.schema.json",
    "talking_cards": "talking_cards.schema.json",
    "tribes": "tribes.schema.json",
}


def project_root() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parents[2]


def schema_dir() -> Path:
    return project_root() / "schemas" / "jsoncardloader"


def load_schema(kind: str) -> dict:
    try:
        filename = SCHEMA_FILES[kind]
    except KeyError as exc:
        logger.exception("Unknown schema kind requested: %s", kind)
        raise ValueError(f"Unknown schema kind: {kind}") from exc
    path = schema_dir() / filename
    logger.debug("Loading schema kind=%s path=%s", kind, path)
    with path.open("r", encoding="utf-8") as handle:
        schema = json.load(handle)
    logger.debug("Loaded schema kind=%s title=%s top_level_keys=%s", kind, schema.get("title"), sorted(schema))
    return schema


def validate_output(kind: str, data: dict) -> list[str]:
    logger.debug("Validating output kind=%s keys=%s", kind, sorted(data) if isinstance(data, dict) else type(data))
    schema = load_schema(kind)
    validator_cls = validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
    formatted = [format_error(error) for error in errors]
    if formatted:
        logger.debug("Validation failed kind=%s error_count=%s errors=%s", kind, len(formatted), formatted)
    else:
        logger.debug("Validation passed kind=%s", kind)
    return formatted


def format_error(error) -> str:
    path = ".".join(str(part) for part in error.path)
    if path:
        return f"{path}: {error.message}"
    return error.message


def sanitize_filename(value: str, fallback: str = "output") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    cleaned = cleaned.strip("._")
    result = cleaned or fallback
    logger.debug("Sanitized filename value=%r fallback=%r result=%r", value, fallback, result)
    return result


def normalize_asset_path(path: str) -> str:
    if not path:
        return ""
    normalized = path.strip().replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", normalized) or normalized.startswith("/"):
        result = Path(normalized).name
        logger.debug("Normalized absolute asset path path=%r result=%r", path, result)
        return result
    logger.debug("Normalized relative asset path path=%r result=%r", path, normalized)
    return normalized


def split_csv(value: str) -> list[str]:
    result = [part.strip() for part in value.split(",") if part.strip()]
    logger.debug("Split CSV value=%r result=%s", value, result)
    return result
