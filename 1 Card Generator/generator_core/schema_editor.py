from __future__ import annotations

import copy
import json
import tkinter as tk
from tkinter import ttk, messagebox

from jsonschema import validators


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
        self.text = tk.Text(self, height=height, width=80, wrap=tk.NONE)
        self.text.pack(fill=tk.BOTH, expand=True)
        controls = ttk.Frame(self)
        controls.pack(fill=tk.X, pady=(4, 0))
        ttk.Button(controls, text="Format JSON", command=self.format_json).pack(side=tk.LEFT)
        ttk.Button(controls, text="Validate", command=self.show_validation).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(controls, text="Reset Empty", command=lambda: self.set_value(default_for_schema(schema))).pack(side=tk.LEFT, padx=(6, 0))
        self.status = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.status, foreground="#6a3b00").pack(fill=tk.X, pady=(4, 0))
        self.set_value(initial_value)

    def get_value(self):
        raw = self.text.get("1.0", tk.END).strip()
        if not raw:
            return default_for_schema(self.schema)
        return json.loads(raw)

    def set_value(self, value):
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", json.dumps(value, indent=4, ensure_ascii=False))
        self.status.set("")

    def format_json(self):
        try:
            self.set_value(self.get_value())
        except json.JSONDecodeError as exc:
            self.status.set(f"JSON parse error: {exc}")

    def validation_errors(self):
        value = self.get_value()
        validator_cls = validators.validator_for(self.schema)
        validator_cls.check_schema(self.schema)
        validator = validator_cls(self.schema)
        return sorted(validator.iter_errors(value), key=lambda err: list(err.path))

    def show_validation(self):
        try:
            errors = self.validation_errors()
        except json.JSONDecodeError as exc:
            self.status.set(f"JSON parse error: {exc}")
            return
        if not errors:
            self.status.set("Behavior tree is valid.")
            return
        message = "\n".join(error.message for error in errors[:8])
        self.status.set(f"{len(errors)} validation error(s).")
        messagebox.showerror("Behavior Validation Error", message)

