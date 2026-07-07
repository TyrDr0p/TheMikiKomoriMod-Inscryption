from __future__ import annotations

import copy
import json
import logging
import tkinter as tk
from tkinter import ttk, messagebox

from jsonschema import validators


logger = logging.getLogger(__name__)


def default_for_schema(schema: dict):
    if "default" in schema:
        return copy.deepcopy(schema["default"])
    schema_type = schema.get("type")
    if schema_type == "object":
        return {}
    if schema_type == "array":
        return []
    if schema_type == "integer":
        return 0
    if schema_type == "number":
        return 0.0
    if schema_type == "boolean":
        return False
    return ""


class JSONSchemaTextEditor(ttk.Frame):
    """Schema-aware JSON editor for nested objects/arrays.

    The JSONCardLoader sigil behavior tree is very deep. This widget keeps the
    full behavior surface editable while validating against the exact nested
    schema extracted from the resource generator.
    """

    def __init__(self, master, schema: dict, initial_value, height=16, **kwargs):
        super().__init__(master, **kwargs)
        self.schema = schema
        logger.debug(
            "Creating JSONSchemaTextEditor schema_type=%s height=%s initial_type=%s",
            schema.get("type"),
            height,
            type(initial_value).__name__,
        )
        self.text = tk.Text(self, height=height, width=80, wrap=tk.NONE)
        self.text.pack(fill=tk.BOTH, expand=True)
        controls = ttk.Frame(self)
        controls.pack(fill=tk.X, pady=(4, 0))
        ttk.Button(controls, text="Format JSON", command=self.format_json).pack(side=tk.LEFT)
        ttk.Button(controls, text="Validate", command=self.show_validation).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(controls, text="Reset Empty", command=lambda: self.set_value(default_for_schema(schema))).pack(side=tk.LEFT, padx=(6, 0))
        self.status = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.status, style="Status.TLabel").pack(fill=tk.X, pady=(4, 0))
        self.set_value(initial_value)

    def get_value(self):
        raw = self.text.get("1.0", tk.END).strip()
        if not raw:
            logger.debug("JSON editor empty; returning schema default")
            return default_for_schema(self.schema)
        value = json.loads(raw)
        logger.debug("JSON editor parsed value type=%s raw_bytes=%s", type(value).__name__, len(raw))
        return value

    def set_value(self, value):
        logger.debug("JSON editor set value type=%s value=%s", type(value).__name__, json.dumps(value, ensure_ascii=False))
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", json.dumps(value, indent=4, ensure_ascii=False))
        self.status.set("")

    def format_json(self):
        try:
            logger.info("Formatting nested JSON editor content")
            self.set_value(self.get_value())
        except json.JSONDecodeError as exc:
            logger.warning("Nested JSON format failed: %s", exc)
            self.status.set(f"JSON parse error: {exc}")

    def validation_errors(self):
        value = self.get_value()
        logger.debug("Validating nested JSON editor value type=%s", type(value).__name__)
        validator_cls = validators.validator_for(self.schema)
        validator_cls.check_schema(self.schema)
        validator = validator_cls(self.schema)
        errors = sorted(validator.iter_errors(value), key=lambda err: list(err.path))
        logger.debug("Nested JSON validation completed error_count=%s", len(errors))
        return errors

    def show_validation(self):
        try:
            errors = self.validation_errors()
        except json.JSONDecodeError as exc:
            logger.warning("Nested JSON validation parse error: %s", exc)
            self.status.set(f"JSON parse error: {exc}")
            return
        if not errors:
            logger.info("Nested JSON validation passed")
            self.status.set("Behavior tree is valid.")
            return
        message = "\n".join(error.message for error in errors[:8])
        logger.info("Nested JSON validation failed error_count=%s first_errors=%s", len(errors), message)
        self.status.set(f"{len(errors)} validation error(s).")
        messagebox.showerror("Behavior Validation Error", message)
