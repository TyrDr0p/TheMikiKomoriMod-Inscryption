from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import validators


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
        raise ValueError(f"Unknown schema kind: {kind}") from exc
    with (schema_dir() / filename).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_output(kind: str, data: dict) -> list[str]:
    schema = load_schema(kind)
    validator_cls = validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)
    errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
    return [format_error(error) for error in errors]


def format_error(error) -> str:
    path = ".".join(str(part) for part in error.path)
    if path:
        return f"{path}: {error.message}"
    return error.message


def sanitize_filename(value: str, fallback: str = "output") -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())
    cleaned = cleaned.strip("._")
    return cleaned or fallback


def normalize_asset_path(path: str) -> str:
    if not path:
        return ""
    normalized = path.strip().replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", normalized) or normalized.startswith("/"):
        return Path(normalized).name
    return normalized


def split_csv(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]

